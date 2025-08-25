from argparse import Namespace
from asyncio import sleep
from typing import AnyStr
from unittest.mock import Mock

import pytest
from _pytest.capture import CaptureFixture

import main
from sample import GOOD_IP, RELAYS_ALL, RELAYS, RELAYS_RESULT
from settings import settings


class FakeWriter:

    def close(self) -> None:
        ...

    async def wait_closed(self) -> None:
        ...


async def fake_open_connection(
        address: str,
        port: int
) -> tuple[None, FakeWriter] | None:
    if address in GOOD_IP:
        return None, FakeWriter()
    else:
        await sleep(settings.TIMEOUT + 1)
        return None


def fake_output() -> None:
    main.relays_lst.sort(
        key=lambda x: x.advertised_bandwidth if x.advertised_bandwidth is not None else 0, reverse=True
    )
    assert main.relays_lst == RELAYS_ALL


async def test_relays_lst(mocker: Mock) -> None:
    mock_open_connection = mocker.AsyncMock(
        side_effect=fake_open_connection
    )
    mocker.patch("asyncio.open_connection", mock_open_connection)

    mock_response = mocker.MagicMock()
    mock_response.return_value.text = RELAYS

    mock_output = mocker.MagicMock(
        side_effect=fake_output
    )

    mocker.patch("main.output", mock_output)
    await main.main(main.parse(mock_response()))


@pytest.mark.parametrize(
    "bandwidth, guard_relays, top, orbot, browser, result_index", [
        (False, False, False, False, False, 0),
        (True, False, False, False, False, 1),
        (False, True, False, False, False, 2),
        (True, True, False, False, False, 3),
        (False, False, True, False, False, 4),
        (False, False, False, False, True, 5),
        (False, False, False, True, False, 6),

    ]
)
def test_relays_filter(
        bandwidth: bool,
        guard_relays: bool,
        top: bool,
        orbot: bool,
        browser: bool,
        result_index: int,
        capsys: CaptureFixture[AnyStr],
        mocker: Mock
) -> None:
    args = Namespace(
        bandwidth=bandwidth, guard_relays=guard_relays, top=top, silent=False, orbot=orbot, browser=browser
    )
    mocker.patch("main.args", args)
    mocker.patch("features.args", args)
    main.output()
    captured = capsys.readouterr()
    assert captured.out == RELAYS_RESULT[result_index]
