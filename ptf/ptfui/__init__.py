from flask import Flask, send_from_directory

app = Flask(__name__)


# Svelte index
@app.route("/")
def base():
    print(app.root_path)
    return send_from_directory("dist", "index.html")


# Svelte routes
@app.route("/<path:path>")
def home(path):
    return send_from_directory("dist", path)


if __name__ == "__main__":
    app.run(debug=True, port=8051)
