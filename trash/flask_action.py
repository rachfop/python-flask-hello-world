from flask import Flask, request

app = Flask(__name__)


@app.route("/subscribe", methods=["GET", "POST"])
def subscribe():
    if request.method == "POST":
        # get the email address from the request
        email = request.form["email"]

        # store the email address in the database or file

        # return a response indicating that the subscription was successful
        return "Thanks for subscribing!"
    else:
        # return a form for the user to enter their email address
        return """
        <form action="/subscribe" method="POST">
            <label for="email">Enter your email address:</label>
            <input type="email" id="email" name="email">
            <input type="submit" value="Subscribe">
        </form>
        """


@app.route("/unsubscribe", methods=["GET", "POST"])
def unsubscribe():
    if request.method == "POST":
        # get the email address from the request
        email = request.form["email"]

        # remove the email address from the database or file

        # return a response indicating that the unsubscription was successful
        return "You have been unsubscribed."
    else:
        # return a form for the user to enter their email address
        return """
        <form action="/unsubscribe" method="POST">
            <label for="email">Enter your email address:</label>
            <input type="email" id="email" name="email">
            <input type="submit" value="Unsubscribe">
        </form>
        """


@app.route("/reoccurring", methods=["GET"])
def reoccurring():
    # code to handle the reoccurring email request goes here
    return "Reoccurring email sent!"
