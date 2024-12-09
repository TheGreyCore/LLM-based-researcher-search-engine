from flask import Flask, request
from service import Service

app = Flask(__name__)

service = Service()


@app.route("/prompt")
def hello_world():
    prompt = request.args.get("prompt")
    if request.args.get("key") != "forTesting":
        return "Invalid key"
    if prompt is None or len(prompt) < 15:
        return "Invalid prompt. Please provide a prompt with at least 15 characters."
    return str(service.processPrompt(prompt))
