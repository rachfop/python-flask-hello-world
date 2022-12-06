# python-flask-hello-world
A Temporal instance using Flask

# Hello World

This is a "Hello World".

## Create an environnement

```bash
python3 -m venv venv
```

## Activate your environment

```bash
. venv/bin/activate
```

## install Flask

```bash
pip3 install Flask
```

## Install Flask's async library

```bash
pip install "Flask[async]"
```

## Update pip

```bash
pip install --upgrade pip
# python -m pip install -U pip
```

## Install Temporal's Python SDK

```python
python -m pip install temporalio
```

## Run the application

```bash
flask --app run_flask run
```

## Install the Temporal CLI

```brew
brew install temporal
```

## Start the Temporal Server

```bash
temporal server start-dev
```

## Terminate Temporal Workflow

```bash
tctl workflow terminate --workflow-id hello-activity-workflow-id
```
