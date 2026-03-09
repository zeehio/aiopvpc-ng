[![PyPI Version][pypi-image]][pypi-url]
[![pre-commit.ci Status][pre-commit-ci-image]][pre-commit-ci-url]
[![Build Status][build-image]][build-url]

<!-- Badges -->

[pypi-image]: https://img.shields.io/pypi/v/aiopvpc-ng
[pypi-url]: https://pypi.org/project/aiopvpc-ng/
[pre-commit-ci-image]: https://results.pre-commit.ci/badge/github/zeehio/aiopvpc-ng/master.svg
[pre-commit-ci-url]: https://results.pre-commit.ci/latest/github/zeehio/aiopvpc-ng/master
[build-image]: https://github.com/zeehio/aiopvpc-ng/actions/workflows/main.yml/badge.svg
[build-url]: https://github.com/zeehio/aiopvpc-ng/actions/workflows/main.yml

# aiopvpc-ng

Fork of [azogue/aiopvpc](https://github.com/azogue/aiopvpc) due to upstream inactivity.

Simple aio library to download Spanish electricity hourly prices.

Made to support the [**`pvpc_hourly_pricing`** HomeAssistant integration](https://www.home-assistant.io/integrations/pvpc_hourly_pricing/).

## Install

Install with `pip install aiopvpc-ng` or clone it to run tests or anything else.

## Usage

```python
import aiohttp
from datetime import datetime
from aiopvpc_ng import PVPCData

async with aiohttp.ClientSession() as session:
    pvpc_handler = PVPCData(session=session, tariff="2.0TD")
    esios_data = await pvpc_handler.async_update_all(
        current_data=None, now=datetime.utcnow()
    )
print(esios_data.sensors["PVPC"])
```
