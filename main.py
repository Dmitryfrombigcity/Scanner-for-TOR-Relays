import argparse
import asyncio
import sys
import urllib.parse
from asyncio import sleep, CancelledError
from itertools import count, cycle
from typing import Any

import requests

from schemas import Relays, Relay
from settings import BASEURL, HEADERS, settings

number = count(start=1)
semaphore: asyncio.Semaphore = asyncio.Semaphore(settings.OPEN_FILES)
relays_lst: list[Relay] = []


def grab() -> requests.Response:
    urls = [
        BASEURL,
        # "https://icors.vercel.app/?" + urllib.parse.quote(BASEURL),
        "https://github.com/Dmitryfrombigcity/tor-onionoo-mirror/raw/master/details-running-relays.json"

    ]
    for url in urls:
        try:
            with requests.get(url, timeout=settings.TIMEOUT, headers=HEADERS) as response:
                response.raise_for_status()
                return response
        except BaseException:
            ...
    print("Didn't get a list of relays")
    sys.exit(1)


def callback(task: asyncio.Task[Any]) -> None:
    if (not task.cancelled()
            and not task.exception()):
        relay = task.result()
        if relay:
            relays_lst.append(relay)


def output_(
        bandwidth: bool,
        guard_relays: bool,
        top: bool
) -> None:
    """Split for test purpose"""

    print("\r         "
          "address                          "
          "fingerprint                "
          "country_name   "
          "first_seen "
          "guard_probability advertised_bandwidth"
          )
    global relays_lst

    if top:
        relays_lst = relays_lst[:5]
        temp: list[str] = []

    for relay in relays_lst:
        if bandwidth and relay.advertised_bandwidth or guard_relays and relay.guard_probability \
                or not (bandwidth or guard_relays):
            print(
                f"{next(number):3d}. "
                f"{relay.or_addresses.ip4:<21} "
                f"{relay.fingerprint:<40} "
                f"{relay.country_name[:14] if relay.country_name is not None else '':^15}  "
                f"{relay.first_seen[:10] if relay.first_seen is not None else ''} "
                f"{relay.guard_probability if relay.guard_probability is not None else 0:13.7f}    "
                f"{relay.advertised_bandwidth / 1049000 if relay.advertised_bandwidth is not None else 0:10.2f} MiB/s"
            )
        if top:
            temp.append(f"{relay.or_addresses.ip4} {relay.fingerprint}\n")
    if top:
        print("\n********************************* Replace bridges for Tor Browser *********************************\n")
        print(*temp, sep='')
        print("*********************************** Replace bridges for torrc ***************************************\n")
        for item in temp[:3]:
            print(f"Bridge {item}", end='')
        print("UseBridges 1")


def output() -> None:
    relays_lst.sort(
        key=lambda x: x.advertised_bandwidth if x.advertised_bandwidth is not None else 0, reverse=True
    )
    output_(args.bandwidth, args.guard_relays, args.top)


def parse(response: requests.Response) -> list[Relay]:
    try:
        data = Relays.model_validate_json(response.text)
        return data.relays
    except Exception as err:
        print(err.__repr__())
        sys.exit(1)


async def progress_bar() -> None:
    hide_cursor = '\x1b[?25l'
    show_cursor = '\x1b[?25h'
    samples = ('⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽')
    items = cycle(samples)
    try:
        while True:
            await sleep(0.5)
            print(f'{hide_cursor}\rAnalysis in progress {next(items)}', end='')
    except CancelledError:
        print(show_cursor)


async def main(relays: list[Relay]) -> None:
    try:
        progress = asyncio.create_task(progress_bar())
        async with asyncio.TaskGroup() as group:
            for relay in relays:
                group.create_task(connect(relay)).add_done_callback(callback)
    except BaseException:
        print(
            '>>> Reduce the OPEN_FILES value in settings.py to avoid the "Too many open files" error.'
        )
    else:
        progress.cancel()
        output()


async def connect(relay: Relay) -> Relay | None:
    async with semaphore:
        try:
            address, port = relay.or_addresses.ip4.split(":")
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(address, port), settings.TIMEOUT)
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
        '-g',
        '--guard',
        dest='guard_relays',
        action='store_const',
        const=True,
        default=False,
        help='display only relays with positive guard_probability'
    )
    parser.add_argument(
        '-b',
        '--bandwidth',
        dest='bandwidth',
        action='store_const',
        const=True,
        default=False,
        help='display only relays with positive advertised_bandwidth'
    )
    parser.add_argument(
        '-t',
        '--top',
        dest='top',
        action='store_const',
        const=True,
        default=False,
        help='display only the top five relays and input templates'
    )
    args = parser.parse_args()
    asyncio.run(main(parse(grab())))
