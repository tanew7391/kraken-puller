from krakenAPI import API
from dotmap import DotMap


class KrakenUtils(object):

    def __init__(self):
        self.api = API()
        self.previousOHLC = None

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

    def get_ohlc(self, currency_one, currency_two, interval=1, since=None, useLastOHLC=False):
        pair = currency_one + currency_two
        input = {}
        input['pair'] = pair
        input['interval'] = interval
        if since and not useLastOHLC:
            input['since'] = since
        elif useLastOHLC:
            input['since'] = self.previousOHLC

        self.api.public(method='OHLC', input=input)
        response = DotMap(self.api.response.json())

        if response.error:
            raise Exception(response.error)

        i = 0
        for _, data in response.result.items():
            if i == 0:
                returnObject = data
            elif i == 1:
                self.previousOHLC = data
            else:
                break
            i += 1

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