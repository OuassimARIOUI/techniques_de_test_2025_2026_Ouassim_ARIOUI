from flask import Flask

app = Flask(__name__)

@app.get("/triangulate/<pointset_id>")
def triangulate(pointset_id):
    return "Not Implemented", 501
