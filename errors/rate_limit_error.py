from .base_api_error import BaseApiError

class RateLimitError(BaseApiError):
    """
        This error is intended to handle 409 (CONFLICT) responses returned
        from VeryCoolStockPriceApi.com's API when it finds our systems have
        sent too many requests at once. It could have been 429 (TOO MANY REQUESTS)
        but we didn't design that server, so here we are.
    """
    pass