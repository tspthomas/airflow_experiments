# Airflow Experiments

This repo was created for an assignment of the Big Data Infrasctructure class (prof. Tiago Ferretto).
It contains simple Airflow examples to showcase some functionality, with a base setup using `uv` for package management.

This is based on the original `docker-compose.yaml` from Airflow's tutorials, with a few changes for our specific examples.

- [Airflow Experiments](#airflow-experiments)
  - [Getting Started](#getting-started)
    - [Requirements](#requirements)
    - [Initial Setup](#initial-setup)
    - [Starting the System](#starting-the-system)
  - [DAGs](#dags)
  - [References](#references)



## Getting Started

### Requirements

TBD - docker setup.

### Initial Setup

TBD - .env setup.

### Starting the System

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

TBD - detail the implemented DAGs


## References

TBD