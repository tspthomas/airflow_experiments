# -*- coding: utf-8 -*-
"""
This DAG computes the square root of numbers in files.
It loads files from a specified directory, computes the square roots of the numbers in those files,
writes the results to a new file, and then deletes the original files.
"""

import os
import math
import pendulum
import logging

from airflow.sdk import dag, task


logger = logging.getLogger(__name__)


@task
def load_files() -> list:
    """Load files from the raw data directory.

    This task scans the raw data directory for files containing "_sqrt.txt" in their names,
    and returns a list of their paths.

    Returns:
        A list of file paths that match the criteria.
    """
    raw_data_dir = os.getenv("RAW_DATA_DIR")
    logger.info(f"Loading file from '{raw_data_dir}'")

    files = []
    for file in os.listdir(raw_data_dir):
        if "_sqrt.txt" not in file:
            continue

        logger.info(file)
        files.append(os.path.join(raw_data_dir, file))

    logger.info(f"Loaded {len(files)} files from '{raw_data_dir}'")
    return files


@task
def compute_sqrt(files: list) -> dict:
    """Compute the square root of numbers in the provided files.

    Args:
        files: A list of file paths containing numbers to process.

    Returns:
        A dictionary where keys are file paths and values are lists of computed square roots.
    """
    processed_files = {}
    logger.info(len(files))
    for f in files:
        with open(f) as fh:
            processed_files[f] = []
            for line in fh.readlines():
                sqrt = math.sqrt(float(line))
                processed_files[f].append(sqrt)

    return processed_files


@task
def write_file(processed_files: dict) -> None:
    """Write the computed square roots to new files.

    Args:
        processed_files: A dictionary where keys are file paths and values are lists of computed square roots.
    """
    processed_data_dir = os.getenv("PROCESSED_DATA_DIR")
    dest = processed_data_dir + "/" + pendulum.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(dest, exist_ok=True)

    for filename, numbers in processed_files.items():
        logger.info(filename)
        name = filename[filename.rindex("/") + 1 :]
        logger.info(name)
        with open(os.path.join(dest, name), "w") as fh:
            for number in numbers:
                fh.write(f"{str(number)}\n")


@task
def delete_files(files: list) -> None:
    """Delete the original files after processing.

    Args:
        files: A list of file paths to delete.
    """
    for filename in files:
        os.remove(filename)


@dag(
    schedule=None,
    start_date=pendulum.datetime(2025, 6, 10, tz="UTC"),
    tags=["square-root", "simple"],
)
def compute_square_root() -> None:
    """
    DAG to compute the square root of numbers in files.

    This DAG loads files from a specified directory, computes the square roots of the numbers in those files,
    writes the results to a new file, and then deletes the original files.
    """
    files = load_files()
    processed_files = compute_sqrt(files)
    write_file(processed_files) >> delete_files(files)


compute_square_root()
