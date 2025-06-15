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
def compute_sqrt():
    logger.info(f"File available. Loading file '{MONITORED_FILEPATH}'")
    results = []
    with open(MONITORED_FILEPATH) as fh:
        for line in fh.readlines():
            sqrt = math.sqrt(float(line))
            results.append(sqrt)

    return results


@task
def write_results_file(results):
    dest = RESULTS_FOLDER + "/" + pendulum.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(dest, exist_ok=True)

    with open(os.path.join(dest, MONITORED_FILENAME), "w") as fh:
        for number in results:
            fh.write(f"{str(number)}\n")


@dag(
    schedule=None,
    start_date=pendulum.datetime(2025, 6, 10, tz="UTC"),
    tags=["square-root", "sensor"],
)
def compute_square_root_sensor():
    wait_for_file = FileSensor(
        task_id="wait_for_file",
        filepath=MONITORED_FILENAME,
        poke_interval=20,  # check every 20 seconds
        mode="poke",  # can be 'poke' or 'reschedule',
        fs_conn_id="fs_monitor_conn",
    )

    results = wait_for_file >> compute_sqrt()
    write_results_file(results)


compute_square_root_sensor()
