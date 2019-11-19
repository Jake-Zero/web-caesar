from flask import Flask, request, redirect
import html
from caesar import rotate_string

app = Flask(__name__)
app.config["DEBUG"] = True

form = """
<!doctype html>
<html>
    <head>
        <style>
            form {{
                background-color: #eee;
                padding: 20px;
                margin: 0 auto;
                width: 540px;
                font: 16px sans-serif;
                border-radius: 10px
            }}
            textarea {{
                margin: 10px 0;
                width: 540px;
                height: 120px;
            }}
        </style>
    </head>
    <body>
        <!-- create your form here -->
        <form method="POST">
            <label> Rotate by:
                <input type="text" name="rot" value="0">
            </label>
            <textarea name="text">{0}</textarea>
            <input type="submit" value="Submit query">
        </form>
    </body>
</html>
"""

@app.route("/")
def index():
    return form.format("")

@app.route("/", methods=["post"])
def encrypt():
    rot = request.form["rot"]
    text = request.form["text"]
    encryption = rotate_string(text, int(rot))
    return form.format(encryption)

@app.route("/hello", methods=["post"])
def hello():
    first_name = request.form["first_name"]
    return "<h1>Hello, " + html.escape(first_name) + "</h1>"

time_form = """
    <style>
        .error {{ color: red; }}
    </style>
    <h1>Validate Time</h1>
    <form method="POST">
        <label>Hours (24-hour format)
            <input name="hours" type="text" value='{hours}' />
        </label>
        <p class="error">{hours_error}</p>
        <label>Minutes
            <input name="minutes" type="text" value='{minutes}' />
        </label>
        <p class="error">{minutes_error}</p>
        <input type="submit" value="Validate" />
    </form>
    """

@app.route("/validate-time")
def display_time_form():
    return time_form.format(hours="", hours_error="", minutes="", minutes_error="")

def is_integer(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

@app.route("/validate-time", methods=["POST"])
def validate_time():

    hours = request.form["hours"]
    minutes = request.form["minutes"]

    hours_error = ""
    minutes_error = ""

    if not is_integer(hours):
        hours_error = "Not a valid integer"
        hours = ""
    else:
        hours = int(hours)
        if hours > 23 or hours < 0:
            hours_error = "Hour value out of range (0-23)"
            hours = ""

    if not is_integer(minutes):
        minutes_error = "Not a valid integer"
        minutes = ""
    else:
        minutes = int(minutes)
        if minutes > 59 or minutes < 0:
            minutes_error = "Minute value out of range (0-59)"
            minutes = ""

    if not minutes_error and not hours_error:
        time = str(hours) + ":" + str(minutes)
        return redirect("/valid-time?time={0}".format(time))
    else:
        return time_form.format(hours_error=hours_error, minutes_error=minutes_error, hours=hours, minutes=minutes)

@app.route("/valid-time")
def valid_time():
    time = request.args.get("time")
    return "<h1>You submitted {0}. Thank you for returning a valid time.</h1>".format(time)

app.run()