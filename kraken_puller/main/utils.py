from krakenAPI import API
from dotmap import DotMap


class KrakenUtils(object):

    def __init__(self):
        self.api = API()
        self.previousOHLC = None
        self.previousRecentTrade = None
        self.previousSpread = None
        self.api.load_key('secret.key')

    def __public_api_grab(self, method, input={}):
        self.api.public(method, input)
        response = DotMap(self.api.response.json())

        if response.error:
            raise Exception(response.error)

        return response.result

    def get_time(self, timeMode='unix'):
        response = self.__public_api_grab(method='Time')
        if timeMode == 'rfc1123':
            return response.rfc1123
        else:
            return response.unixtime

    def get_all_assets(self):
        return self.__public_api_grab(method='Assets')

    def get_pair_info(self, currency_one, currency_two, info=None):
        input = {}
        pair = currency_one + currency_two
        input['pair'] = pair
        if info:
            input['info'] = info

        response = self.__public_api_grab(method='AssetPairs', input=input)

        for _, data in response.items():  # allows a bypass to the name pair, allowing for a STANDARD object (XXBTCAD=Object just returns object without needing the XXBTCAD part)
            returnObject = data
            break

        return returnObject

    def get_ticker_info(self, currency_one, currency_two):
        pair = currency_one + currency_two
        input = {}
        input['pair'] = pair

        response = self.__public_api_grab(method='Ticker', input=input)

        for _, data in response.items():  # allows a bypass to the name pair, allowing for a STANDARD object
            returnObject = data
            break

        return returnObject

    def __get_data_helper(self, pair, method, input=None, since=None):
        if not input:
            input = {}
        input['pair'] = pair
        if since:
            input['since'] = since

        response = self.__public_api_grab(method=method, input=input)

        i = 0
        for _, data in response.items():
            if i == 0:
                returnObject = data
            elif i == 1:
                returnPrevious = data
            else:
                break
            i += 1

        return returnObject, returnPrevious

    def get_ohlc(self, currency_one, currency_two, interval=1, since=None, useLastOHLC=False):
        pair = currency_one + currency_two
        input = {}
        input['interval'] = interval

        if useLastOHLC and not since:
            since = self.previousOHLC

        returnObject, self.previousOHLC = self.__get_data_helper(pair, method='OHLC', input=input, since=since)

        return returnObject
        
    def get_order_book(self, currency_one, currency_two, count=None):
        pair = currency_one + currency_two
        input = {}
        input['pair'] = pair
        if count:
            input['count'] = count

        response = self.__public_api_grab(method='Depth', input=input)
 
        for _, data in response.items():  # allows a bypass to the name pair, allowing for an unambiguous object
            returnObject = data
            break

        return returnObject

    def get_recent_trades(self, currency_one, currency_two, since=None, usePreviousRecentTrade=False):
        pair = currency_one + currency_two

        if usePreviousRecentTrade and not since:
            since = self.previousOHLC

        returnObject, self.previousRecentTrade = self.__get_data_helper(pair, 'Trades', since=since)

        return returnObject

    def get_spread_data(self, currency_one, currency_two, since=None, usePreviousSpread=False):
        pair = currency_one + currency_two

        if usePreviousSpread and not since:
            since = self.previousSpread

        returnObject, self.previousSpread = self.__get_data_helper(pair, 'Spread', since=since)

        return returnObject

    def __private_api_grab(self, method, input={}):
        self.api.private(method, input=input)
        response = DotMap(self.api.response.json())
        if response.error:
            raise Exception(response.error)

        return response.result

    def get_account_balence(self):
        return self.__private_api_grab(method='Balance')

    def get_trade_balance(self, asset_class=None, base_currency=None):
        input = {}
        if asset_class:
            input['aclass'] = asset_class  # default is currency
        if base_currency:
            input['asset'] = base_currency  # default is USD

        return self.__private_api_grab(method='TradeBalance', input=input)

    def get_open_orders(self, boolTrades=None, userref=None):
        input = {}
        if boolTrades:
            input['trades'] = 'true'
        if userref:
            input['userref'] = userref

        return self.__private_api_grab(method='OpenOrders', input=input)

    def get_closed_orders(self, **kwargs):  # trades=false, userref=None, starttime=None, endtime=None, offset=None, closetime=None
        input = {}
        if len(kwargs) > 0:
            input = kwargs

        return self.__private_api_grab(method='ClosedOrders', input=input)

    def __txid_reader(self, txid):
        final = txid[0]
        for ids in txid[1:]:
            final += ', ' + ids
        input = {
            'txid': final
        }

        return input


    def query_orders_info(self, txid, trades=False, userref=None):
        input = self.__txid_reader(txid)

        if trades:
            input['trades'] = 'true'
        if userref:
            input['userref'] = userref
        print(input)

        return self.__private_api_grab(method='QueryOrders', input=input)

    def get_trades_history(self, **kwargs):
        input = {}
        if len(kwargs) > 0:
            input = kwargs

        return self.__private_api_grab(method='TradesHistory', input=input)

    def query_trades_info(self, txid, trades=None):
        input = self.__txid_reader(txid)

        if trades:
            input['trades'] = 'true'

        return self.__private_api_grab(method='QueryTrades', input=input)

    def get_open_positions(self, txid, docalcs=False, consolidation=None):
        input = self.__txid_reader(txid)

        if docalcs:
            input['docals'] = 'true'
        if consolidation:
            input['consolidation'] = consolidation

        return self.__private_api_grab(method='OpenPositions', input=input)

    def get_ledgers_info(self, **kwargs):
        input = {}
        if len(kwargs) > 0:
            input = kwargs

        return self.__private_api_grab(method='Ledgers', input=input)


