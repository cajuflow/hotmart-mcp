"""
Data models for Hotmart API responses

NOTE: This file is deprecated. Use individual model files instead:
- hotmart.models.product.Product
- hotmart.models.sale.Sale  
- hotmart.models.subscription.Subscription
- hotmart.models.base.ApiResponse, AuthToken
"""

# Import from new modular structure for backward compatibility
from .models.base import *
from .models.product import *
from .models.sale import *
from .models.subscription import *

# This file will be removed in future versions
# Please update imports to use:
# from hotmart.models.product import Product
# from hotmart.models.sale import Sale
# etc.
