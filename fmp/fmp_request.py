
# +---------+
# | Imports |
# +---------+

import requests
from typing import Optional, override
import json
from pathlib import Path
import pandas as pd


# +---------------+
# | Request Class |
# +---------------+

class FMPRequest:
    API_KEY_NAME = 'financial_modeling_prep_dcl'

    def __init__(self, request_type: str,
                 symbol: str,
                 api_key: Optional[str] = None):
        self.request_type = request_type.lower()
        self.symbol = symbol.upper()
        self._api_key = api_key

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        if value is None:
            self._api_key = FMPRequest.get_api_key(self.API_KEY_NAME)
        elif isinstance(value, str):
            if value.lower().startswith('financial_modeling_prep'):
                self._api_key = FMPRequest.get_api_key(value)
            else:
                self._api_key = value

    @property
    def url(self):
       return (f'https://financialmodelingprep.com/stable/'
               f'{self.request_type}'
               f'?symbol={self.symbol}'
               f'&apikey={self.api_key}')

    def get(self, output_format: str = 'json'):
        result = requests.get(self.url).json()

        if output_format == 'json':
            return result
        elif output_format == 'pandas':
            return pd.DataFrame(result)
        else:
            raise ValueError("Valid output format: ['json' | 'pandas']")

    @staticmethod
    def get_api_key(api_key_name: str, key_file: Path = None) -> str | None:
        if key_file is None:
            key_file = Path.cwd() / 'api_ops' / 'apikeys.json'

        try:
            with open(key_file, 'r') as f:
                keys = json.load(f)
                key = keys[api_key_name]
                return key
        except FileNotFoundError:
            print(f'File "{key_file}" was not found')


class DemoFMPRequest(FMPRequest):
    API_KEY_NAME = None

    @override
    @property
    def api_key(self):
        return None

    @override
    @api_key.setter
    def api_key(self, value):
        self._api_key = None

    @override
    @property
    def url(self):
        """Mimics FMP API call via demo_api_calls.json

        Whereas normally, .url would define the URL endpoint for an FMP API call
        to get a JSON string, here .url uses demo_api_calls.json to directly
        import a saved sample API call as a Python dict object.
        """
        with open(Path.cwd() / 'fmp/demo_api_calls.json') as f:
            return json.load(f)[self.symbol][self.request_type]

    @override
    def get(self, output_format: str = 'json'):
        result = self.url  # dict object

        if output_format == 'json':
            return result
        elif output_format == 'pandas':
            return pd.DataFrame(result)
        else:
            raise ValueError("Valid output format: ['json' | 'pandas']")
