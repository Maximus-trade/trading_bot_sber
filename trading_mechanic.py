import get_candles
import get_portfolio
import timing_exchange
from _datetime import datetime
import time
from tinkoff.invest import Client, OrderDirection, OrderType, Quotation, TimeInForceType, PriceType, OperationType
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
print('input the interval')
b = int(input())
print('input the price increase')
increase = float(input())
print('input the price decrease')
decrease = float(input())

FIGI = 'BBG004730N88'
INSTRUMENT = 'e6123145-9665-43e0-8413-cd61b8aa9b13'

#figi = FIGI, SBER
# r = client.instruments.shares()
# r = client.instruments.get_assets # doesn't work at all
#get_candles.main()


while True:
    timing_exchange.is_within_time_range()
    time.sleep(b)
    get_candles.last_price()
    ops_list = get_candles.get_orders()
    operations_obj = get_portfolio.get_ops()
    print(operations_obj)
    print(ops_list.orders == [])
    rub_sv = operations_obj[0].units
    kop_sv = operations_obj[0].nano
    price_order = 0
    price_order = rub_sv + (kop_sv * 0.000000001)
    rub: int = get_candles.rub
    kop: float = get_candles.kop
    d = rub + (kop*0.000000001)
    if operations_obj[1] == OperationType.OPERATION_TYPE_BUY and price_order + ((price_order/100)*increase) <= d and ops_list.orders == []:
        get_candles.order_send_sell()
        print('limit order sent, type: SELL')
    elif operations_obj[1] == OperationType.OPERATION_TYPE_SELL and price_order - ((price_order/100)*decrease) >= d and ops_list.orders == []:
        get_candles.order_send()
        print('limit order sent, type: BUY')
    else:
        print('last operation: ', operations_obj[1])
        print('last price: ', d)
        print('last operation price: ', price_order)
        print('price to reach in case of growth: ', price_order + ((price_order/100)*increase))
        print('price to reach in case of fall: ', price_order - ((price_order/100)*decrease))