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
INSTRUMENT = 'BBG004730N88' #SBER
YDEX = 'BBG0047' #YDEX


def get_portf():
    with Client(TOKEN) as client:
        r = client.operations.get_portfolio(account_id='2166394631')
    print(r)

get_portf()



# YDEX = 'TCS00A107T19' FIGI
# SBERP = BBG0047315Y7 FIGI
# SBER = BBG004730N88 FIGI
# TBND = TCS00A1039N1 FIGI
# 1fbecbbc-ef32-448c-b4fe-b0037795ba01 sovkombank UID FIGI TCS00A0ZZAC4
# e6123145-9665-43e0-8413-cd61b8aa9b13 sber UID
#'664070a8-55bd-42c4-9172-836eb52da5c4' instrument_uid=  YDEX
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
