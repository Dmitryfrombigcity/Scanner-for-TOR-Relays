from asyncio import sleep
from typing import AnyStr
from unittest.mock import Mock

import pytest
from _pytest.capture import CaptureFixture

import main
from main import relays_lst
from settings import settings
from tests.sample import GOOD_IP, RELAYS_ALL, RELAYS, RELAYS_RESULT


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
    assert relays_lst == RELAYS_ALL


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
    "bandwidth, guard_relays, result_index", [
        (False, False, 0),
        (True, False, 1),
        (False, True, 2),
    ]
)
def test_relays_filter(
        bandwidth: bool,
        guard_relays: bool,
        result_index: int,
        capsys: CaptureFixture[AnyStr]
) -> None:
    main.output_(bandwidth, guard_relays)
    captured = capsys.readouterr()
    assert captured.out == RELAYS_RESULT[result_index]
