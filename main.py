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

app.run()