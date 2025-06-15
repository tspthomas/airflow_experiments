import os
import math
import pendulum
import logging

from airflow.sdk import dag, task


logger = logging.getLogger(__name__)


@task()
def load_files():
    raw_data_dir = os.getenv("RAW_DATA_DIR")
    logger.info(f"Loading file from '{raw_data_dir}'")

    files = []
    for file in os.listdir(raw_data_dir):
        if ".txt" not in file:
            continue

        logger.info(file)
        files.append(os.path.join(raw_data_dir, file))

    logger.info(f"Loaded {len(files)} files from '{raw_data_dir}'")
    return files


@task
def compute_sqrt(files: list):
    processed_files = {}
    for f in files:
        with open(f) as fh:
            processed_files[f] = []
            for line in fh.readlines():
                sqrt = math.sqrt(float(line))
                processed_files[f].append(sqrt)

    return processed_files


@task
def write_file(processed_files):
    processed_data_dir = os.getenv("PROCESSED_DATA_DIR")
    dest = processed_data_dir + "/" + pendulum.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(dest, exist_ok=True)

    for filename, numbers in processed_files.items():
        name = filename[filename.rindex("/") + 1 :]
        with open(os.path.join(dest, name), "w") as fh:
            for number in numbers:
                fh.write(f"{str(number)}\n")


@dag(
    schedule=None,
    start_date=pendulum.datetime(2025, 6, 10, tz="UTC"),
    tags=["square-root", "simple"],
)
def compute_square_root():
    files = load_files()
    processed_files = compute_sqrt(files)
    write_file(processed_files)


compute_square_root()
