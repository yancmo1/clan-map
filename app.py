from flask import Flask, render_template
from map_generator import generate_map

app = Flask(__name__)

@app.route("/")
def index():
    generate_map()
    return render_template("map.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5010)
