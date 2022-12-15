# python-flask-hello-world

## run_flask

This code is a Python script that uses the Flask web framework to create a simple web application. The application processes an email form submissions and another to return the contents of a file called `index.html`.

When the script runs, it creates a Flask app instance and defines two routes for the app. The first route is a function called `get_data`, which uses the `asyncio` module to run an async function called main in a separate thread. The main function returns some data, which is used to render a `Jinja2` template called `index.html`. This template is then returned as the response to the route.

The second route is a function called `process_email_form`, which is called whenever an HTTP POST request is made to the app's root URL (i.e. `/`). This function processes the form data that was submitted in the request, and depending on the value of the action field, either adds the email address to a list of subscribers or removes it from the list. In either case, it sends an email to the user using the `send_email` function defined in the `Email` class.

The `Email` class is used to send emails using the `smtplib` module. It expects the email address and password to be stored in environment variables called `EMAIL_ADDRESS` and `EMAIL_PASSWORD`, respectively. If these variables are not set, the `send_email` function will not be able to send emails. The `send_email` function uses the `smtplib` module to send an email using the Gmail SMTP server.

Overall, this script defines a simple Flask app that provides a form for users to subscribe or unsubscribe from an email list, and sends confirmation emails to users when they submit the form.

## run_worker

This code is a Python script that uses the `asyncio` module to implement an asynchronous Workflow using the `temporalio` package. The script defines two classes: `SubscribeStatus` and `GreetingWorkflow`, and an async function called `main`.

The `SubscribeStatus` class is a simple dataclass that has a single field called `status`, which is a string representing the current subscription status of a user (either `subscribed` or `unsubscribed`).

The `GreetingWorkflow` class defines a Workflow that sends a monthly email to a user for a year. The workflow is implemented as an async method called `run`, which takes a status argument and returns a string representing the final subscription status of the user. The run method uses the `execute_activity` function provided by the `temporalio` package to execute an async function called `send_monthly_email` in a separate thread. The `send_monthly_email` function sends an email using the `send_email` function defined in the `Email` class and waits for a month before sending the next email. If the status argument is `unsubscribed`, the `send_monthly_email` function returns immediately without sending any emails, essentially unsubscribing the user from any further emails.

The `main` function is the entry point of the script. It creates a `Client` instance and uses it to start a `Worker` instance that can execute the `GreetingWorkflow` Workflow and the `send_monthly_email` activity. The main function then uses the `Client` instance to execute the `GreetingWorkflow.run` method and returns the result.

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

## Install the Temporal CLI

```brew
brew install temporal
```

## Start the Temporal Server

```bash
temporal server start-dev
```

## Terminate Temporal Workflow

To terminate a Workflow, run the follow tctl command.

```bash
temporal workflow terminate --workflow-id hello-activity-workflow-id
temporal workflow terminate --workflow-id my-workflow-id
```

## Export environment variables

```bash
export FLASK_APP=run_flask.py
export FLASK_DEBUG=true
```

## Create Email environment variables

```bash
pip install python-dotenv
```

Export your email address and password in a `.env` file.

```bash
EMAIL_ADDRESS=my-gmail-address@gmail.com
EMAIL_PASSWORD=app-password-for-gmail
```

For information on how to create a Gmail App Password, see [Sign in with App Passwords](https://support.google.com/accounts/answer/185833).

## Run the application

```bash
flask run
# flask --app run_flask run
```
