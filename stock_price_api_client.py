import requests, time
from errors import NotFoundError, RateLimitError

class StockPriceApiClient:
    """
    This is an API client for handling the gathering of price data
    from VeryCoolStockPriceAPI.com.
    """
    API_URL = "http://127.0.0.1:8080"
    API_RATE_LIMIT = 1 # request/second

    """
        Get the price of a ticker. Ticker must be ascii letter characters only.
    """
    @classmethod
    def get_ticker_price(cls, ticker):
        response = requests.get(f"{cls.API_URL}/lookupPrice/{ticker.upper()}")
        if response.ok:
            return response.json()
            # Since this is a developer-centric api client, it makes sense to return
            # the raw prices, which can have many more than 2 decimal points
            # ("prices" usually only get as granular as the penny). If we just leave
            # the data as-is, the business can make decisions further up the stack about
            # how to display prices in whatever way they (we?) choose
            #
            # But if we wanted to we could round to the nearest penny:
            # price = float(json["price"])
            # return f"{ticker} price: {round(price, 2)}"
        elif response.status_code == 209:
            raise RateLimitError(
                f"""
                    We've sent too many requests.
                    Wait {cls.API_RATE_LIMIT} seconds before trying again
                """
            )
        elif response.status_code == 404:
            raise NotFoundError(
                f"""
                    Ticker {ticker} could not be found or is invalid,
                    please ensure it is comprised of a maximum of
                    four (4) ascii letters [a-zA-Z] (e.g. 'aapl', 'TSLA', etc.)
                """
            )
        else:
            raise "Something has gone horribly, horribly wrong. Call the police."

    """
        Fetch the price for a ticker continuously,
        1.1 second/req so we don't hit the rate limit (1 second).
        Ticker must be ascii letter characters only.
        The data is available for manipulation/storage for each iteration, like so:
        ```python
        for json_blob in StockPriceApiClient.poll_ticker_price():
            print(f"{json_blob["symbol"]} price: {round(json_blob["price"], 2)}")
        ```
    """
    @classmethod
    def poll_ticker_price(cls, ticker):
        buffer = 0.1 # 10% buffer seems safe, generally
        while True:
            try:
                yield cls.get_ticker_price(ticker.upper())
                time.sleep(cls.API_RATE_LIMIT + buffer)
            except RateLimitError:
                time.sleep(buffer) # snooze button
                yield cls.get_ticker_price(ticker.upper())