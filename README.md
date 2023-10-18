# Stock Price API mini-project

The purpose of this repo is to show an example of a stock price api that has the following limitations:
    1. The server has a rate limit of 1 req/s
    2. Any concurrent requests will fail with 409 (CONFLICT)

The API client is written in python, using only built-in packages (requests)

## Instructions / How to use

Start the server (requires [node](https://github.com/nodejs/node) to be installed):
```
node stock_price_server.js
```
In another terminal session, navigate to the root of the project, and ensure the path is injected into your environments PYTHONPATH
```
cd ~/path/to/project/stock_price_api
export PYTHONPATH=$PYTHONPATH:~/path/to/project/stock_price_api
```

Start the python REPL
```
python
```
import the API client, and fire away!
```
>>> from .stock_price_api_client import StockPriceApiClient
>>>
>>> client = StockPriceApiClient
>>> client.get_ticker_price('TSLA')
{'price': 0.4352897234905, 'symbol': 'TSLA'}
>>>
>>> for json_blob in client.poll_ticker_price():
>>>     print(f"{json_blob['symbol']} price: {round(json_blob['price'], 2)}")
TSLA price: 0.66
TSLA price: 0.46
TSLA price: 0.82
TSLA price: 0.76
TSLA price: 0.98
...
```

This API is just about as random as the actual stock market!