from utils import KrakenUtils

funcs = KrakenUtils()

#print(funcs.get_time(timeMode='rfc1123'))

#l = funcs.get_all_assets()

#for s in l:
 #   print(s)

#print(funcs.get_pair_info(currency_one='xbt', currency_two='cad'))
#print(funcs.get_ticker_info(currency_one='xbt', currency_two='cad'))
#print(funcs.get_ohlc(currency_one='xbt', currency_two='cad'))
#print(funcs.get_order_book(currency_one='xbt', currency_two='cad'))
#print(funcs.get_recent_trades(currency_one='xbt', currency_two='cad'))
#print(funcs.previousRecentTrade)
print(funcs.get_spread_data(currency_one='xbt', currency_two='cad'))
