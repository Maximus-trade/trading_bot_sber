import get_candles
import get_portfolio
from _datetime import datetime
import time
from tinkoff.invest import Client, OrderDirection, OrderType, Quotation, TimeInForceType, PriceType, OperationType
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TOKEN')



FIGI = 'BBG004730N88'
INSTRUMENT = 'e6123145-9665-43e0-8413-cd61b8aa9b13'

#figi = FIGI, SBER
# r = client.instruments.shares()
# r = client.instruments.get_assets # doesn't work at all
#get_candles.main()




a = True
while a:
    time.sleep(3)
    get_candles.last_price()
    operations_obj = get_portfolio.get_ops()
    print(operations_obj)
    rub_sv = operations_obj[0].units
    kop_sv = operations_obj[0].nano
    price_order = 0
    price_order = rub_sv + (kop_sv * 0.000000001)
    rub: int = get_candles.rub
    kop: float = get_candles.kop
    d = rub + (kop*0.000000001)
    if operations_obj[1] == OperationType.OPERATION_TYPE_BUY and price_order + ((price_order/100)*0.9) <= d:
        get_candles.order_send_sell()
    elif operations_obj[1] == OperationType.OPERATION_TYPE_SELL and price_order - ((price_order/100)*0.9) >= d:
        get_candles.order_send()
    else:
        print('last operation: ', operations_obj[1])
        print('last price: ', d)
        print('last operation price: ', price_order)