# -*- coding: utf-8 -*-
"""
This DAG summarizes text files using a pre-trained model.
It loads files from a specified directory, summarizes their content using a model,
writes the summaries to new files, and deletes the original files.
"""

import os
import pendulum
import logging

from airflow.sdk import dag, task
from transformers import pipeline


logger = logging.getLogger(__name__)

MODEL = "facebook/bart-large-cnn"


@task()
def load_files() -> list:
    """Load files from the raw data directory.

    This task scans the raw data directory for files containing "_summary.txt" in their names,
    and returns a list of their paths.

    Returns:
        A list of file paths that match the criteria.
    """
    raw_data_dir = os.getenv("RAW_DATA_DIR")
    logger.info(f"Loading file from '{raw_data_dir}'")

    files = []
    for file in os.listdir(raw_data_dir):
        if "_summary.txt" not in file:
            continue

        logger.info(file)
        files.append(os.path.join(raw_data_dir, file))

    logger.info(f"Loaded {len(files)} files from '{raw_data_dir}'")
    return files


@task
def summarize(files: list) -> dict:
    """Summarize the content of the provided text files using a pre-trained model.

    Args:
        files: A list of file paths containing text to summarize.

    Returns:
        A dictionary where keys are file paths and values are the summaries of the content.
    """
    summarizer = pipeline("summarization", model=MODEL)
    summaries = {}
    for f in files:
        with open(f) as fh:
            content = fh.readlines()

            summary = summarizer(content)
            summaries[f] = summary[0]["summary_text"]

    return summaries


@task
def write_files(summaries: dict) -> None:
    """Write the summaries to new files in a timestamped directory.

    Args:
        summaries: A dictionary where keys are file paths and values are the summaries of the content.
    """
    if len(summaries) == 0:
        logger.info("No summaries to write.")
        return

    processed_data_dir = os.getenv("PROCESSED_DATA_DIR")
    dest = processed_data_dir + "/" + pendulum.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(dest, exist_ok=True)

    for filename, summary in summaries.items():
        name = filename[filename.rindex("/") + 1 :]
        with open(os.path.join(dest, name), "w") as fh:
            fh.writelines(summary)


@task
def delete_files(processed_files: list) -> None:
    """Delete the original files after processing.

    Args:
        processed_files: A list of file paths to delete.
    """
    for filename in processed_files:
        os.remove(filename)


@dag(
    schedule=None,
    start_date=pendulum.datetime(2025, 6, 10, tz="UTC"),
    tags=["ml", "summarization"],
)
def summarize_text() -> None:
    """
    DAG to summarize text files using a pre-trained model.

    This DAG loads files from a specified directory, summarizes their content using a model,
    writes the summaries to new files, and deletes the original files.
    """
    files = load_files()
    summaries = summarize(files)
    write_files(summaries) >> delete_files(files)


summarize_text()
