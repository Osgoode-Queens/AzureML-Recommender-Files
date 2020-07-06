from flask import Flask, render_template, request, redirect, url_for, flash
import urllib
import json

app = Flask(__name__)

# Variable
# Replace this with the API key for the web service
api_key = 'B8G1BENqkF49KyIJCmw+Eiidb4swkj6jnDRQwerzyQNTAnK+bMif3zBCjRuKZ6are8j2KpIBz6RV8dNNpEzHJg=='
# Replace this with your endpoint
url = 'https://ussouthcentral.services.azureml.net/workspaces/dcc90e1a3a5b4a0929ffeeeafcceed93/services' \
      '/5dff9c905c4b4f55bc3339719c7205b3/execute?api-version=2.0&details=true'


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user = request.form["searchBar"]
        return redirect(url_for("getUser", usr=user))
    else:
        return render_template("index.html")

@app.route("/<usr>", methods=["GET", "POST"])
def getUser(usr):
    if request.method == "POST":
        user = request.form["searchBar"]
        return redirect(url_for("getUser", usr=user))
    else:
        restaurantList = getUserRestaurant(usr)
        return render_template("user.html", user=usr, items=restaurantList)

def getUserRestaurant(user):
    #define request
    restaurantList = []
    data = {
        "Inputs": {
            "input1":
                {
                    "ColumnNames": ["userID"],
                    "Values": [[user]]
                }, },
        "GlobalParameters": {
        }
    }
    body = str.encode(json.dumps(data))
    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        restaurantList = result.get('Results').get('output1').get('value').get('Values')[0]
    except urllib.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

    return restaurantList


if __name__ == "__main__":
    app.run(debug=True)