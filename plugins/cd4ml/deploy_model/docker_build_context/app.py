import flask

app = flask.Flask(__name__)

if __name__ == "__main__":
    from score import score
    
    @app.route("/", methods=["GET", "POST"])
    def flask_wrapper():
        return flask.jsonify(score.run(flask.request.json))
    
    score.init()
    app.run(host="0.0.0.0")