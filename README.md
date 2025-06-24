# Airflow Experiments

This repo was created for an assignment of the Big Data Infrasctructure class (prof. Tiago Ferretto).
It contains simple Airflow examples to showcase some functionality, with a base setup using `uv` for package management.

This is based on the original `docker-compose.yaml` from Airflow's tutorials, with a few changes for our specific examples.

> [!WARNING]
> This repo is not supposed to be used in production. This is just a sample repository to showcase simple scenarios using Airflow. For production deployment, please check the official documentation - https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/production-deployment.html.


## Index

- [Airflow Experiments](#airflow-experiments)
  - [Index](#index)
  - [Getting Started](#getting-started)
    - [Requirements](#requirements)
    - [Initial Setup](#initial-setup)
    - [Starting the System](#starting-the-system)
  - [DAGs](#dags)



## Getting Started

### Requirements

* Install `Docker` following instructions from their official website - https://docs.docker.com/engine/install/.
    * `Docker Compose` should be already available. In case it is not, please check the instructions here - https://docs.docker.com/compose/install/.
* Install `uv` for managining Python packages and projects. Follow the instructions in their official website - http://docs.astral.sh/uv/getting-started/installation/.

### Initial Setup

* Create the .env file in your root folder (do not version this file in git)
  ```bash
  touch .env
  ```
* Add your `AIRFLOW_UID` to it
  ```bash
  echo -e "AIRFLOW_UID=$(id -u)" >> .env
  ```
* Add two required environment variables to map local folders
  ```bash
  echo -e "RAW_DATA_DIR=/workspace/data/raw/" >> .env
  echo -e "PROCESSED_DATA_DIR=/workspace/data/processed/" >> .env
  ```

At the end, you should have something like this (`AIRFLOW_UID` might be different)

```bash
AIRFLOW_UID=501
RAW_DATA_DIR=/workspace/data/raw/
PROCESSED_DATA_DIR=/workspace/data/processed/
```

### Starting the System

Ensure you have started Docker Desktop.

Build the Docker images

```bash
docker compose build
```

Start the containers

```bash
docker compose up
```

In case you want to stop

```bash
docker compose down
```

You may also want to remove all the data from volumes. In this case, you can execute the following:

```bash
docker compose down --volumes --remove-orphans
```


## DAGs

This repository contains simple DAGs to illustrate given functionalities in Airflow.
It contains the following DAGs:
* `dags/sqrt/`
    * `compute_sqrt_simple.py`: simple example that reads a file from `data/raw` with a number in each line and generates a file with the corresponding square root, stored in `data/processed`. File must end with `_sqrt.txt`.
    * `compute_sqrt_sensor.py`: simple example that monitors a given file in a folder using `Sensor`. When a file named `monitored_file.txt` is placed inside `data/monitor`, this DAG will process it accordingly.
* `dags/ml/`
    * `summarize_text.py`: simple example that reads a file from `data/raw` with a given text and summarizes it into anoter file using an LLM, storing the resulting file in `data/processed`. File must end with `_summary.txt`.