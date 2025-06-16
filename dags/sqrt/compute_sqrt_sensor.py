# -*- coding: utf-8 -*-
"""
This DAG monitors a file and computes the square root of its contents.
It waits for a specific file to appear, reads numbers from it,
computes their square roots, writes the results to a new file,
and deletes the original monitored file.
"""

import os
import math
import pendulum
import logging

from airflow.sdk import dag, task
from airflow.sensors.filesystem import FileSensor


logger = logging.getLogger(__name__)

MONITORED_FILENAME = "monitored_file.txt"
MONITORED_FILEPATH = os.path.join(os.getenv("MONITOR_DATA_DIR"), MONITORED_FILENAME)
RESULTS_FOLDER = os.getenv("PROCESSED_DATA_DIR")


@task
def compute_sqrt() -> list:
    """Compute the square root of numbers in a monitored file.

    This task reads numbers from a file, computes their square roots,
    and returns the results.

    Returns:
        A list of square roots of the numbers read from the file.
    """
    logger.info(f"File available. Loading file '{MONITORED_FILEPATH}'")
    results = []
    with open(MONITORED_FILEPATH) as fh:
        for line in fh.readlines():
            sqrt = math.sqrt(float(line))
            results.append(sqrt)

    return results


@task
def write_results_file(results: list) -> None:
    """Write the computed square roots to a results file.

    Args:
        results: A list of square roots to write to the results file.
    """
    dest = RESULTS_FOLDER + "/" + pendulum.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(dest, exist_ok=True)

    with open(os.path.join(dest, MONITORED_FILENAME), "w") as fh:
        for number in results:
            fh.write(f"{str(number)}\n")


@task
def delete_file() -> None:
    """Delete the monitored file after processing."""
    os.remove(MONITORED_FILEPATH)


@dag(
    schedule=None,
    start_date=pendulum.datetime(2025, 6, 10, tz="UTC"),
    tags=["square-root", "sensor"],
)
def compute_square_root_sensor() -> None:
    """
    DAG to monitor a file and compute the square root of its contents.

    This DAG uses a FileSensor to wait for the presence of a file,
    computes the square root of each number in the file, writes the results
    to a new file, and deletes the original monitored file.
    """
    wait_for_file = FileSensor(
        task_id="wait_for_file",
        filepath=MONITORED_FILENAME,
        poke_interval=20,  # check every 20 seconds
        mode="poke",  # can be 'poke' or 'reschedule',
        fs_conn_id="fs_monitor_conn",
    )

    results = wait_for_file >> compute_sqrt()
    write_results_file(results) >> delete_file()


compute_square_root_sensor()
