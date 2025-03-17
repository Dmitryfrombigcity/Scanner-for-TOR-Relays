import argparse
import asyncio
import sys
import urllib.parse
from itertools import count

import requests

from schemas import Relays, Relay
from settings import BASEURL, TIMEOUT, HEADERS, OPEN_FILES

number = count(start=1)
semaphore: asyncio.Semaphore = asyncio.Semaphore(OPEN_FILES)


def grab() -> requests.Response:
    urls = [
        "https://icors.vercel.app/?" + urllib.parse.quote(BASEURL),
        BASEURL,
    ]
    for url in urls:
        try:
            with requests.get(url, timeout=TIMEOUT, headers=HEADERS) as response:
                return response
        except:
            ...
    print("Didn't get a list of relays")
    sys.exit(1)


def callback(task: asyncio.Task) -> None:
    if (not task.cancelled()
            and not task.exception()):
        relay = task.result()
        if relay:
            print(
                f"{next(number):3d}. "
                f"{relay.or_addresses.ip4:<21} "
                f"{relay.fingerprint:<40} "
                f"{relay.country_name[:14]:^15}  "
                f"{relay.first_seen[:10]} "
                f"{0 if relay.guard_probability is None else relay.guard_probability:13.7f}    "
                f"{relay.advertised_bandwidth / 1049000:10.2f} MiB/s"
            )


def parse(response: requests.Response) -> list[Relay]:
    try:
        data = Relays.model_validate_json(response.text)
        return data.relays
    except Exception as err:
        print(err.__repr__())
        sys.exit(1)


async def main(relays: list[Relay]) -> None:
    try:
        async with asyncio.TaskGroup() as group:
            for relay in relays:
                # In Tor metrics We Trust
                if relay.guard_probability or args.all_relays:
                    group.create_task(connect(relay)).add_done_callback(callback)
    except BaseException:
        print(
            '>>> Reduce the OPEN_FILES value in settings.py to avoid the "Too many open files" error.'
        )


async def connect(relay: Relay) -> Relay | None:
    async with semaphore:
        try:
            address, port = relay.or_addresses.ip4.split(":")
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(address, port), TIMEOUT)
            writer.close()
            await writer.wait_closed()
        except asyncio.TimeoutError:
            return None
        except OSError as err:
            if err.args[-1] == 'Too many open files':
                raise
            return None
        else:
            return relay


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a',
        '--all',
        dest='all_relays',
        action='store_const',
        const=True,
        default=False,
        help='display all relays'
    )
    args = parser.parse_args()
    print("         "
          "address                          "
          "fingerprint                "
          "country_name   "
          "first_seen "
          "guard_probability advertised_bandwidth"
          )
    asyncio.run(main(parse(grab())))
