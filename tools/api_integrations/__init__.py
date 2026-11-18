"""
API Integrations Module

Provides integrations with popular APIs:
- Zalo
- Telegram
- Facebook
- Google
- Shopee

Usage:
    from api_integrations import ZaloClient, TelegramBot, FacebookClient, GoogleClient, ShopeeClient
    
    # Zalo
    from zalo_integration import ZaloClient
    client = ZaloClient(access_token="YOUR_TOKEN")
    client.send_message(user_id="USER_ID", message="Hello")
    
    # Telegram
    from telegram_integration import TelegramBot
    bot = TelegramBot(bot_token="BOT_TOKEN")
    bot.send_message(chat_id=123456, text="Hello")
    
    # Facebook
    from facebook_integration import FacebookClient
    client = FacebookClient(access_token="TOKEN")
    client.post_to_page(page_id="PAGE_ID", message="Hello")
    
    # Google
    from google_integration import GoogleClient
    client = GoogleClient(credentials_path="credentials.json")
    client.gmail_list_messages()
    
    # Shopee
    from shopee_integration import ShopeeClient
    client = ShopeeClient(partner_id="ID", partner_key="KEY", shop_id=123)
    client.get_order_list()
"""

from .zalo_integration import ZaloClient, ZaloConfig
from .telegram_integration import TelegramBot, TelegramConfig
from .facebook_integration import FacebookClient, FacebookConfig
from .google_integration import GoogleClient, GoogleConfig
from .shopee_integration import ShopeeClient, ShopeeConfig
from .sepay_integration import SePayClient, SePayConfig
from .payos_integration import PayOSClient, PayOSConfig
from .pay2s_integration import Pay2SClient, Pay2SConfig
from .payment_aggregator import (
    PaymentAggregator,
    AccountQuota,
    PaymentRoutingResult,
    ManualReceiptSubmission,
    RoutingStatus,
    ManualPaymentStatus,
)

__all__ = [
    "ZaloClient",
    "ZaloConfig",
    "TelegramBot",
    "TelegramConfig",
    "FacebookClient",
    "FacebookConfig",
    "GoogleClient",
    "GoogleConfig",
    "ShopeeClient",
    "ShopeeConfig",
    "SePayClient",
    "SePayConfig",
    "PayOSClient",
    "PayOSConfig",
    "Pay2SClient",
    "Pay2SConfig",
    "PaymentAggregator",
    "AccountQuota",
    "PaymentRoutingResult",
    "ManualReceiptSubmission",
    "RoutingStatus",
    "ManualPaymentStatus",
]

