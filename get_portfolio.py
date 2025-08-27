import time
from datetime import timedelta
from typing import List, Any
from tinkoff.invest import CandleInterval, Client, InstrumentRequest, OperationsRequest, OperationState
from tinkoff.invest.services import InstrumentsService, MarketDataService, OperationsService
from tinkoff.invest.utils import now
import os
from dotenv import load_dotenv
import get_portfolio

global r
global k
load_dotenv()
TOKEN = os.getenv('TOKEN')
INSTRUMENT = 'BBG004730N88'


def get_portf():
    with Client(TOKEN) as client:
        r = client.operations.get_portfolio(account_id='2166394631')
    print(r)





# SBERP = BBG0047315Y7 FIGI
# SBER = BBG004730N88 FIGI
# TBND = TCS00A1039N1 FIGI


def get_ops():
    ops = []
    with Client(TOKEN) as client:
        t = client.operations.get_operations(
            account_id='2166394631',
            from_=now() - timedelta(days=50),
            to=now(),
            state=OperationState.OPERATION_STATE_EXECUTED,
            figi=INSTRUMENT)
        for i in range(len(t.operations)):
            if t.operations[i].price.units > 0:
                ops.append(t.operations[i].price)
                ops.append(t.operations[i].operation_type)
                ops.append(t.operations[i].date)
            else:
                continue
            return ops
