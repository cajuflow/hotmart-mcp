#!/usr/bin/env python3
"""
Hotmart MCP Server

A Model Context Protocol server for integrating with Hotmart APIs.
Provides tools for managing products, sales, and other Hotmart operations.
"""

import sys
import asyncio
from io import TextIOWrapper
from pathlib import Path

# Configure encoding for Windows compatibility
if sys.platform == "win32":
    try:
        sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = TextIOWrapper(sys.stderr.buffer, encoding="utf-8")
    except AttributeError:
        sys.stdout = TextIOWrapper(sys.stdout.detach(), encoding="utf-8")
        sys.stderr = TextIOWrapper(sys.stderr.detach(), encoding="utf-8")

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import logging
from mcp.server.fastmcp import FastMCP

from hotmart.config import (
    HOTMART_ENVIRONMENT, BASE_URL, TRANSPORT_TYPE, MCP_HOST, MCP_PORT
)
from hotmart.tools import get_products, get_sales_history

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("hotmart-mcp")

# Initialize FastMCP
mcp = FastMCP(
    name="Hotmart MCP Server",
    host=MCP_HOST,
    port=MCP_PORT
)


@mcp.tool()
async def get_hotmart_products(
    status: str = None,
    max_results: int = 50,
    page_token: str = None,
    product_id: str = None,
    format: str = None
) -> str:
    """
    Get list of products from Hotmart account.
    
    Args:
        status: Filter by product status. Options: DRAFT, ACTIVE, PAUSED, NOT_APPROVED, IN_REVIEW, DELETED, CHANGES_PENDING_ON_PRODUCT
        max_results: Maximum number of items per page (default: 50, max: 50)
        page_token: Cursor for pagination
        product_id: Unique identifier (ID) of the product (7 digits)
        format: Product format. Options: EBOOK, SOFTWARE, MOBILE_APPS, VIDEOS, AUDIOS, TEMPLATES, IMAGES, ONLINE_COURSE, SERIAL_CODES, ETICKET, ONLINE_SERVICE, ONLINE_EVENT, BUNDLE, COMMUNITY
    
    Returns:
        JSON string containing list of products with their details
    """
    return await get_products(status, max_results, page_token, product_id, format)


@mcp.tool()
async def get_hotmart_sales_history(
    transaction_status: str = None,
    max_results: int = 50,
    page_token: str = None,
    product_id: str = None,
    start_date: str = None,
    end_date: str = None,
    sales_source: str = None,
    transaction: str = None,
    buyer_name: str = None,
    buyer_email: str = None,
    payment_type: str = None,
    offer_code: str = None,
    commission_as: str = None
) -> str:
    """
    Get sales history from Hotmart account.
    
    Args:
        transaction_status: Status da transação. Options: APPROVED, BLOCKED, CANCELLED, CHARGEBACK, COMPLETE, EXPIRED, NO_FUNDS, OVERDUE, PARTIALLY_REFUNDED, PRE_ORDER, PRINTED_BILLET, PROCESSING_TRANSACTION, PROTESTED, REFUNDED, STARTED, UNDER_ANALISYS, WAITING_PAYMENT
        max_results: Número máximo de itens por página (default: 50, max: 50)
        page_token: Cursor para paginação
        product_id: ID do produto (7 dígitos)
        start_date: Data inicial em milissegundos (timestamp desde 1970-01-01)
        end_date: Data final em milissegundos (timestamp desde 1970-01-01)
        sales_source: Código SRC da origem da venda
        transaction: Código único da transação (ex: HP17715690036014)
        buyer_name: Nome do comprador
        buyer_email: Email do comprador
        payment_type: Tipo de pagamento. Options: BILLET, CASH_PAYMENT, CREDIT_CARD, DIRECT_BANK_TRANSFER, DIRECT_DEBIT, FINANCED_BILLET, FINANCED_INSTALLMENT, GOOGLE_PAY, HOTCARD, HYBRID, MANUAL_TRANSFER, PAYPAL, PAYPAL_INTERNACIONAL, PICPAY, PIX, SAMSUNG_PAY, WALLET
        offer_code: Código da oferta
        commission_as: Como foi comissionado. Options: PRODUCER, COPRODUCER, AFFILIATE
    
    Returns:
        JSON string containing sales history with detailed information
    """
    return await get_sales_history(
        transaction_status, max_results, page_token, product_id,
        start_date, end_date, sales_source, transaction,
        buyer_name, buyer_email, payment_type, offer_code, commission_as
    )

async def server_main():
    """Asynchronously runs the main server logic."""
    # This function can be expanded for more complex startup sequences
    run_server()

def run_server():
    """
    Detects the transport mode from environment variables and starts the
    MCP server accordingly.
    """
    # Show startup information to stderr (visible in Claude Desktop logs)
    print("Starting Hotmart MCP Server", file=sys.stderr)
    print(f"Environment: {HOTMART_ENVIRONMENT}", file=sys.stderr)
    print(f"API Base URL: {BASE_URL}", file=sys.stderr)
    print(f"Transport mode selected: {TRANSPORT_TYPE.upper()}", file=sys.stderr)
    print("=" * 50, file=sys.stderr)

    if TRANSPORT_TYPE == "sse":
        print(f"-> Running in SSE mode on {MCP_HOST}:{MCP_PORT}", file=sys.stderr)
        mcp.run(transport="sse")
    elif TRANSPORT_TYPE == "stdio":
        print("-> Running in STDIO mode for local integration", file=sys.stderr)
        mcp.run(transport="stdio")
    else:
        print(
            f"FATAL: Invalid TRANSPORT_TYPE '{TRANSPORT_TYPE}'. Must be 'stdio' or 'sse'.",
            file=sys.stderr
        )
        sys.exit(1)

if __name__ == "__main__":
    run_server()
