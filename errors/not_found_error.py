from .base_api_error import BaseApiError

class NotFoundError(BaseApiError):
    """
        This error is intended to handle 404 (NOT FOUND) responses returned
        from VeryCoolStockPriceApi.com's API when it encounters an
        invalid/nonexistent ticker
    """
    pass