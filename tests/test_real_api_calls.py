"""Tests for aiopvpc_ng."""

import os
from datetime import datetime
from typing import cast
from zoneinfo import ZoneInfo

import pytest
from aiohttp import ClientSession

from aiopvpc_ng import PVPCData
from aiopvpc_ng.const import ALL_SENSORS, DataSource, KEY_PVPC, REFERENCE_TZ
from tests.conftest import TZ_TEST


async def _get_real_data(
    timezone: ZoneInfo, data_source: str, indicators: tuple[str, ...], ts: datetime
):
    if data_source == "esios":
        api_token = os.getenv("ESIOS_TOKEN")
        if api_token is None:
            pytest.skip("ESIOS_TOKEN missing, skipping test.")
    else:
        api_token = None
    async with ClientSession() as session:
        pvpc_data = PVPCData(
            session=session,
            tariff="2.0TD",
            local_timezone=timezone,
            api_token=api_token,
            data_source=cast(DataSource, data_source),
            sensor_keys=indicators,
        )
        return await pvpc_data.async_update_all(None, ts)


@pytest.mark.real_api_call
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data_source, timezone, num_sensors",
    (
        ("esios", REFERENCE_TZ, 6),
        ("esios", TZ_TEST, 6),
        ("esios_public", REFERENCE_TZ, 1),
        ("esios_public", TZ_TEST, 1),
    ),
)
async def test_real_download_today_async(data_source, timezone, num_sensors):
    sensor_keys = ALL_SENSORS if data_source == "esios" else (KEY_PVPC,)
    api_data = await _get_real_data(
        timezone, data_source, sensor_keys, datetime.utcnow()
    )
    assert 22 < len(api_data.sensors[KEY_PVPC]) < 49
    assert len(api_data.sensors) == num_sensors


if __name__ == "__main__":
    import asyncio
    from dataclasses import asdict
    from pprint import pprint

    # timestamp = datetime(2021, 10, 30, 21)
    timestamp = datetime.utcnow()
    api_data = asyncio.run(
        _get_real_data(REFERENCE_TZ, "esios", ALL_SENSORS, timestamp)
    )
    pprint(asdict(api_data))
