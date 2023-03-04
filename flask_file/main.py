from flask import Flask
import server
from deta import Deta

db = Deta(project_key="c0h15t2h_vGPSZCu2Zaqnw6bgHgFfFVrc6yrju65W")
db = db.Base(name="flask_file")
app = Flask(__name__)
app.secret_key="test"

app.register_blueprint(server.bp)

@app.route("/hello/<name>",methods=["GET"])
def hello_world(name):
    return f"HELLO {name}"
