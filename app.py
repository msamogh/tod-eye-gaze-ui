from pathlib import Path
from pprint import pprint
import json
import os
import random

import click
from flask import Flask, render_template, session, jsonify, request

from data_util import (
    Dialogue,
    load_multiwoz,
    load_star,
    load_multiwoz_ontology,
    load_star_ontology,
)


DIALOGUE_IDX_KEY = "DIALOGUE_IDX"
GAZE_STREAM_PATH = None

MULTIWOZ = load_multiwoz()
STAR = load_star()

ONTOLOGIES = {"STAR": load_star_ontology(), "MULTIWOZ": load_multiwoz_ontology()}


app = Flask(__name__)
app.secret_key = "TERRRIGDENOINDEdfnfw3"


def next_dialogue() -> Dialogue:
    if not session.get(DIALOGUE_IDX_KEY):
        session[DIALOGUE_IDX_KEY] = 0
    # Randomly decide between MultiWOZ and STAR
    if random.random() < 0.5:
        dialogue = random.choice(MULTIWOZ)
    else:
        dialogue = random.choice(STAR)
    session[DIALOGUE_IDX_KEY] += 1
    return dialogue


@app.route("/")
def index():
    dialogue = next_dialogue()
    pprint(dialogue)
    return render_template(
        "index.html",
        dialogue=dialogue,
        slots=ONTOLOGIES[dialogue.dataset][dialogue.domain],
    )


def get_last_line(path):
    with open(path, "rb") as f:
        try:  # catch OSError in case of a one line file
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b"\n":
                f.seek(-2, os.SEEK_CUR)
        except OSError:
            f.seek(0)
        last_line = f.readline().decode()
        return last_line


@app.route("/latest_gaze_coords", methods=["POST"])
def latest_gaze_coords():
    while True:
        try:
            last_line = get_last_line(GAZE_STREAM_PATH)
            latest_log = json.loads(last_line)["values"]["frame"]["avg"]
            # print(f"Latest log: {latest_log}")
            break
        except Exception as e:
            print(e)
            continue
    return jsonify(latest_log)


@app.route("/telemetry", methods=["POST"])
def telemetry():
    # print("Telemetry received")
    # print(request.data)
    try:
        data = json.loads(request.data)
        bounds = data["bounds"]
        time = float(data["timestamp"])
    except:
        pass
    return "success"


@click.command()
@click.argument("gaze-stream-path")
def main(gaze_stream_path):
    global GAZE_STREAM_PATH
    GAZE_STREAM_PATH = gaze_stream_path
    app.run(port=8001, debug=True)


if __name__ == "__main__":
    main()
