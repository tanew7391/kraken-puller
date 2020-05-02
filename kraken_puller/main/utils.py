from krakenAPI import API
from dotmap import DotMap


class KrakenUtils(object):

    def __init__(self):
        self.api = API()
        self.previousOHLC = None
        self.previousRecentTrade = None
        self.previousSpread = None

    def get_time(self, timeMode='unix'):
        self.api.public(method='Time', timeout=2000)
        response = DotMap(self.api.response.json())

        if response.error:
            raise Exception(response.error)

        if timeMode == 'rfc1123':
            return response.result.rfc1123
        else:
            return response.result.unixtime

    def get_all_assets(self):
        self.api.public(method='Assets')
        response = DotMap(self.api.response.json())

        if response.error:
            raise Exception(response.error)

        return response.result

    def get_pair_info(self, currency_one, currency_two, info=None):
        pair = currency_one + currency_two
        input = {}
        if info:
            input['info'] = info
        input['pair'] = pair

        self.api.public(method='AssetPairs', input=input)
        response = DotMap(self.api.response.json())

        if response.error:
            raise Exception(response.error)

        for _, data in response.result.items():  # allows a bypass to the name pair, allowing for a STANDARD object (XXBTCAD=Object just returns object without needing the XXBTCAD part)
            returnObject = data
            break

        return returnObject

    def get_ticker_info(self, currency_one, currency_two):
        pair = currency_one + currency_two
        input = {}
        input['pair'] = pair

        self.api.public(method='Ticker', input=input)
        response = DotMap(self.api.response.json())

        if response.error:
            raise Exception(response.error)

        for _, data in response.result.items():  # allows a bypass to the name pair, allowing for a STANDARD object
            returnObject = data
            break

        return returnObject

    def __get_data_helper(self, pair, method, input=None, since=None):
        if not input:
            input = {}
        input['pair'] = pair
        if since:
            input['since'] = since

        self.api.public(method=method, input=input)
        response = DotMap(self.api.response.json())

        if response.error:
            raise Exception(response.error)

        i = 0
        for _, data in response.result.items():
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

        self.api.public(method='Depth', input=input)
        response = DotMap(self.api.response.json())
        if response.error:
            raise Exception(response.error)

        for _, data in response.result.items():  # allows a bypass to the name pair, allowing for a STANDARD object
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