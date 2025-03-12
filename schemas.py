from typing import NamedTuple

from pydantic import BaseModel


class IPs(NamedTuple):
    ip4: str
    ip6: str | None = None


class Relay(BaseModel):
    fingerprint: str
    or_addresses: IPs
    first_seen: str | None = None
    country_name: str | None = None
    guard_probability: float | None = None
    advertised_bandwidth: int | None = None


class Relays(BaseModel):
    relays: list[Relay]
