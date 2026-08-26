from subprocess import Popen
from typing import Any

from hatchet_sdk.runnables.types import EmptyModel
import pytest

from hatchet_sdk import Hatchet
from tests.thread_pool_exhaust.worker import my_async_task_that_i_do_control


@pytest.mark.parametrize(
    "on_demand_worker",
    [
        [
            "poetry",
            "run",
            "python",
            "tests/thread_pool_exhaust/worker.py",
        ]
    ],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="session")
async def test_thread_pool_exhaust(
    hatchet: Hatchet, on_demand_worker: Popen[Any]
) -> None:
    await my_async_task_that_i_do_control.aio_run_many(
        [
            my_async_task_that_i_do_control.create_bulk_run_item(EmptyModel())
            for _ in range(20)
        ]
    )
