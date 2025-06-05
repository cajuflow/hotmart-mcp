"""
Sales management tool for Hotmart MCP
"""

import json
import logging
from typing import Optional
from datetime import datetime

from .base import api_client, format_error, validate_max_results

logger = logging.getLogger("hotmart-tools.sales")


def validate_transaction_status(status: str) -> str | None:
    """Validate transaction_status parameter"""
    valid_statuses = [
        "APPROVED", "BLOCKED", "CANCELLED", "CHARGEBACK", "COMPLETE", 
        "EXPIRED", "NO_FUNDS", "OVERDUE", "PARTIALLY_REFUNDED", "PRE_ORDER", 
        "PRINTED_BILLET", "PROCESSING_TRANSACTION", "PROTESTED", "REFUNDED", 
        "STARTED", "UNDER_ANALISYS", "WAITING_PAYMENT"
    ]
    if status.upper() not in valid_statuses:
        return f"Invalid transaction_status '{status}'. Valid options are: {', '.join(valid_statuses)}"
    return None


def validate_payment_type(payment_type: str) -> str | None:
    """Validate payment_type parameter"""
    valid_types = [
        "BILLET", "CASH_PAYMENT", "CREDIT_CARD", "DIRECT_BANK_TRANSFER", 
        "DIRECT_DEBIT", "FINANCED_BILLET", "FINANCED_INSTALLMENT", "GOOGLE_PAY", 
        "HOTCARD", "HYBRID", "MANUAL_TRANSFER", "PAYPAL", "PAYPAL_INTERNACIONAL", 
        "PICPAY", "PIX", "SAMSUNG_PAY", "WALLET"
    ]
    if payment_type.upper() not in valid_types:
        return f"Invalid payment_type '{payment_type}'. Valid options are: {', '.join(valid_types)}"
    return None


def validate_commission_as(commission_as: str) -> str | None:
    """Validate commission_as parameter"""
    valid_commissions = ["PRODUCER", "COPRODUCER", "AFFILIATE"]
    if commission_as.upper() not in valid_commissions:
        return f"Invalid commission_as '{commission_as}'. Valid options are: {', '.join(valid_commissions)}"
    return None


async def get_sales_history(
    transaction_status: Optional[str] = None,
    max_results: int = 50,
    page_token: Optional[str] = None,
    product_id: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    sales_source: Optional[str] = None,
    transaction: Optional[str] = None,
    buyer_name: Optional[str] = None,
    buyer_email: Optional[str] = None,
    payment_type: Optional[str] = None,
    offer_code: Optional[str] = None,
    commission_as: Optional[str] = None
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
        JSON string containing list of sales with their details
    """
    try:
        logger.info(f"Fetching sales history with transaction_status={transaction_status}, max_results={max_results}, page_token={page_token}")
        
        # Validate transaction_status parameter
        if transaction_status:
            status_error = validate_transaction_status(transaction_status)
            if status_error:
                return format_error(status_error)
        
        # Validate max_results parameter
        max_results_error = validate_max_results(max_results)
        if max_results_error:
            return format_error(max_results_error)
        
        # Validate payment_type parameter
        if payment_type:
            payment_error = validate_payment_type(payment_type)
            if payment_error:
                return format_error(payment_error)
        
        # Validate commission_as parameter
        if commission_as:
            commission_error = validate_commission_as(commission_as)
            if commission_error:
                return format_error(commission_error)
        
        # Fetch sales from Hotmart API
        response = await api_client.get_sales_history(
            transaction_status=transaction_status,
            max_results=max_results,
            page_token=page_token,
            product_id=product_id,
            start_date=start_date,
            end_date=end_date,
            sales_source=sales_source,
            transaction=transaction,
            buyer_name=buyer_name,
            buyer_email=buyer_email,
            payment_type=payment_type,
            offer_code=offer_code,
            commission_as=commission_as
        )
        
        # Extract sales from response
        items = response.get("items", [])
        page_info = response.get("page_info", {})
        
        # Format response
        result = {
            "total_items": len(items),
            "page_info": page_info,
            "items": []
        }
        
        # Process each sale
        for sale_data in items:
            try:
                # Convert timestamps to readable dates
                purchase = sale_data.get("purchase", {})
                order_date = datetime.fromtimestamp(purchase.get("order_date", 0) / 1000).isoformat()
                approved_date = datetime.fromtimestamp(purchase.get("approved_date", 0) / 1000).isoformat()
                warranty_expire_date = datetime.fromtimestamp(purchase.get("warranty_expire_date", 0) / 1000).isoformat()
                
                sale = {
                    "product": sale_data.get("product", {}),
                    "buyer": sale_data.get("buyer", {}),
                    "producer": sale_data.get("producer", {}),
                    "purchase": {
                        **purchase,
                        "order_date_formatted": order_date,
                        "approved_date_formatted": approved_date,
                        "warranty_expire_date_formatted": warranty_expire_date
                    }
                }
                result["items"].append(sale)
            except Exception as e:
                logger.warning(f"Error processing sale data: {e}")
                continue
        
        # Add summary message
        filters = []
        if transaction_status:
            filters.append(f"status='{transaction_status}'")
        if payment_type:
            filters.append(f"payment='{payment_type}'")
        if buyer_email:
            filters.append(f"buyer='{buyer_email}'")
        if product_id:
            filters.append(f"product_id='{product_id}'")
        
        filter_text = f" with {', '.join(filters)}" if filters else ""
        summary = f"Found {len(items)} sales{filter_text}"
        
        if page_info.get("next_page_token"):
            summary += f". Use page_token='{page_info['next_page_token']}' to get next page."
        if page_info.get("prev_page_token"):
            summary += f" Use page_token='{page_info['prev_page_token']}' for previous page."
        
        result["summary"] = summary
        
        return json.dumps(result, indent=2, ensure_ascii=False)
        
    except Exception as e:
        error_msg = f"Error fetching sales history: {str(e)}"
        logger.error(error_msg)
        return format_error(error_msg)
