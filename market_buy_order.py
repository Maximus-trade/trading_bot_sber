from datetime import datetime
from tinkoff.invest import Client, RequestError, OrderDirection, OrderType, Quotation
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TOKEN')
FIGI = "TCS00A1039N1"

with Client(TOKEN) as client:

    r = client.orders.post_order(
    order_id=str(datetime.utcnow().timestamp()),
    figi=FIGI,
    quantity=1,
    account_id='2166394631',
    direction=OrderDirection.ORDER_DIRECTION_BUY,
    order_type=OrderType.ORDER_TYPE_MARKET
 )