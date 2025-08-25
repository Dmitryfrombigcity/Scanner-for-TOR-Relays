import asyncio
import sys
import urllib.parse
from itertools import count, cycle
from typing import Any

import requests

from arguments import args
from exceptions import TooManyOpenFiles, NetworkIsUnreachable
from features import modify, suppress
from schemas import Relays, Relay
from settings import BASEURL, HEADERS, settings

number = count(start=1)
semaphore: asyncio.Semaphore = asyncio.Semaphore(settings.OPEN_FILES)
relays_lst: list[Relay] = []


def grab() -> requests.Response:
    urls = [
        BASEURL,
        "https://raw.githubusercontent.com/Dmitryfrombigcity/tor-onionoo-mirror/master/details-running-relays.json"
    ]
    for url in urls:
        try:
            with requests.get(url, timeout=settings.TIMEOUT, headers=HEADERS) as response:
                response.raise_for_status()
                return response
        except BaseException as err:
            print(f'# URL:{urllib.parse.urlparse(url).netloc} >> Error:{type(err).__name__}')
    print("Didn't get a list of relays")
    sys.exit(1)


def callback(task: asyncio.Task[Any]) -> None:
    if (not task.cancelled()
            and not task.exception()):
        relay = task.result()
        if relay:
            relays_lst.append(relay)


@modify
def output() -> None:
    global relays_lst
    relays_lst.sort(
        key=lambda x: x.advertised_bandwidth if x.advertised_bandwidth is not None else 0, reverse=True
    )

    print(
        "\r", " " * 9,
        "address", " " * 26,
        "fingerprint", " " * 16,
        "country_name", " " * 3,
        "first_seen", " ",
        "guard_probability advertised_bandwidth",
        sep=""
    )

    if args.top:
        relays_lst = relays_lst[:5]
        temp: list[str] = []

    for relay in relays_lst:
        if (args.bandwidth and relay.advertised_bandwidth and args.guard_relays and relay.guard_probability
                or args.bandwidth and relay.advertised_bandwidth and not args.guard_relays
                or args.guard_relays and relay.guard_probability and not args.bandwidth
                or not (args.bandwidth or args.guard_relays)):
            print(
                f"{next(number):3d}. "
                f"{relay.or_addresses.ip4:<21} "
                f"{relay.fingerprint:<40} "
                f"{relay.country_name[:14] if relay.country_name is not None else '':^15}  "
                f"{relay.first_seen[:10] if relay.first_seen is not None else ''} "
                f"{relay.guard_probability if relay.guard_probability is not None else 0:13.7f}    "
                f"{relay.advertised_bandwidth / 1049000 if relay.advertised_bandwidth is not None else 0:10.2f} MiB/s"
            )
        if args.top:
            temp.append(f"{relay.or_addresses.ip4} {relay.fingerprint}\n")
    if args.top:
        print(
            "\n********************************* Replace bridges for Tor Browser *********************************\n"
        )
        print(*temp, sep='')
        print(
            "*********************************** Replace bridges for Orbot ***************************************\n"
        )
        for item in temp[:3]:
            print(f"Bridge {item}", end='')
        print("UseBridges 1")


def parse(response: requests.Response) -> list[Relay]:
    try:
        data = Relays.model_validate_json(response.text)
        return data.relays
    except Exception as err:
        print(err.__repr__())
        sys.exit(1)


@suppress
async def progress_bar() -> None:
    hide_cursor = '\x1b[?25l'
    show_cursor = '\x1b[?25h'
    samples = ('⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽')
    items = cycle(samples)
    try:
        while True:
            await asyncio.sleep(0.5)
            print(f'{hide_cursor}\rAnalysis in progress {next(items)}', end='')
    except asyncio.CancelledError:
        print(show_cursor)


async def main(relays: list[Relay]) -> None:
    progress: asyncio.Task[None] = asyncio.create_task(progress_bar())
    try:
        async with asyncio.TaskGroup() as group:
            for relay in relays:
                group.create_task(connect(relay)).add_done_callback(callback)

    except* TooManyOpenFiles:
        print(
            '\n>>> Reduce the OPEN_FILES value in settings.py to avoid the "Too many open files" error.'
        )
    except* NetworkIsUnreachable:
        print(
            '\n>>> Network is getting unreachable, try to reduce the OPEN_FILES value in settings.py or something else.'
        )
    except* Exception:
        print(
            '\n>>> Something went wrong.'
        )

    else:
        output()
    finally:
        progress.cancel()


async def connect(relay: Relay) -> Relay | None:
    async with semaphore:
        try:
            address, port = relay.or_addresses.ip4.split(":")
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(address, port), settings.TIMEOUT
            )
            writer.close()
            await writer.wait_closed()
        except asyncio.TimeoutError:
            return None
        except OSError as err:
            if err.args[0] == 24:  # Too many open files
                raise TooManyOpenFiles
            if err.args[0] == 101:  # Network is unreachable
                raise NetworkIsUnreachable
            return None
        else:
            return relay


if __name__ == '__main__':
    try:
        asyncio.run(main(parse(grab())))
    except KeyboardInterrupt:
        print(
            '>>> Interrupted by user.'
        )
