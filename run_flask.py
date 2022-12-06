from flask import Flask
import asyncio

from run_worker import main

app = Flask(__name__)


@app.route("/")
async def get_data():
    result = await main()
    return result


if __name__ == "__main__":
    app.run()
