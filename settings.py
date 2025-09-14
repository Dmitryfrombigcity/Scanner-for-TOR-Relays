import os
from ipaddress import ip_address
from pathlib import Path
from typing import Annotated

from pydantic import PlainValidator
from pydantic_settings import BaseSettings, SettingsConfigDict, NoDecode

BASEURL = ("https://onionoo.torproject.org/details?type=relay&running=true&recommended_version=true&"
           "fields=fingerprint,or_addresses,first_seen,country_name,guard_probability,advertised_bandwidth")
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}


def decode_addresses(value: str) -> set[str]:
    addresses: set[str] = set()
    for address in value.split(','):
        try:
            ip4, port = address.split(':')
            ip_address(ip4.strip())
            if 1 <= int(port) <= 65535:
                addresses.add(f'{ip4.strip()}:{port.strip()}')
        except ValueError:
            print(f'# The blacklist variable has an invalid format >> {address}')
    return addresses


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).parent / '.env', validate_default=False)

    TIMEOUT: int = 5
    OPEN_FILES: int = 1000
    NO_PROXY: str = 'raw.githubusercontent.com'
    BLACKLIST: Annotated[set[str], NoDecode, PlainValidator(decode_addresses)] = set()


settings = Settings()
print(f'# The blacklist >> {settings.BLACKLIST if settings.BLACKLIST else 'empty'}')
os.environ['NO_PROXY'] = settings.NO_PROXY
