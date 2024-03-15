import time
from _datetime import datetime
from datetime import timedelta
from tinkoff.invest import CandleInterval, Client, Quotation, OrderDirection, TimeInForceType, PriceType, OrderType, \
    InstrumentRequest, LastPrice, PortfolioResponse, PositionsResponse, PortfolioPosition
from tinkoff.invest.services import InstrumentsService, MarketDataService
from tinkoff.invest.utils import now
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
INSTRUMENT = 'e6123145-9665-43e0-8413-cd61b8aa9b13'
rub = 0
kop = 0


def main():
    with Client(TOKEN) as client:
        for candle in client.get_all_candles(
                instrument_id="e6123145-9665-43e0-8413-cd61b8aa9b13",
                from_=now() - timedelta(minutes=10),
                interval=CandleInterval.CANDLE_INTERVAL_1_MIN,
        ):
            print(candle)

    return 0


def last_price():
    with Client(TOKEN) as client:
        u = client.market_data.get_last_prices(instrument_id=['e6123145-9665-43e0-8413-cd61b8aa9b13'])
    global rub
    global kop
    rub = u.last_prices[0].price.units
    kop = u.last_prices[0].price.nano
    print(u.last_prices[0].time)
    return rub, kop


def order_send():
    with Client(TOKEN) as client:
        r = client.orders.post_order(
            order_id=str(datetime.utcnow().timestamp()),
            instrument_id=INSTRUMENT,
            price=Quotation(units=rub, nano=kop),
            quantity=1,
            account_id='2166394631',
            direction=OrderDirection.ORDER_DIRECTION_BUY,
            order_type=OrderType.ORDER_TYPE_LIMIT,
            time_in_force=TimeInForceType.TIME_IN_FORCE_DAY,
            price_type=PriceType.PRICE_TYPE_CURRENCY
        )
    print(r)


rub_new = rub
kop_new = kop
print(kop)
print(rub)


def order_send_sell():
    with Client(TOKEN) as client:
        r = client.orders.post_order(
            order_id=str(datetime.utcnow().timestamp()),
            instrument_id=INSTRUMENT,
            price=Quotation(units=rub, nano=kop),
            quantity=1,
            account_id='2166394631',
            direction=OrderDirection.ORDER_DIRECTION_SELL,
            order_type=OrderType.ORDER_TYPE_LIMIT,
            time_in_force=TimeInForceType.TIME_IN_FORCE_DAY,
            price_type=PriceType.PRICE_TYPE_CURRENCY
        )
    print(r)
