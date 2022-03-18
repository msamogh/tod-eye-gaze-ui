from pathlib import Path
from pprint import pprint
import json
import os
import time
import random

import click
from flask import Flask, request, jsonify, render_template, session, redirect, url_for

from data_util import (
    Dialogue,
    load_multiwoz,
    load_star,
    load_multiwoz_ontology,
    load_star_ontology,
)
from constants import (
    NAME_EMAIL_FOLDER,
    GAZE_PATH_FOLDER,
    MULTIWOZ_PRETTY_SLOTS,
    STAR_PRETTY_SLOTS,
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


@app.route("/home", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Save the form data to the session object
        print(request.form)
        session["email"] = request.form["email_address"]
        session["name"] = request.form["name"]
        session["calibration_score"] = request.form["calibration_score"]
        session["session_id"] = f"{int(time.time())}"
        try:
            if not os.path.exists(NAME_EMAIL_FOLDER):
                os.mkdir(NAME_EMAIL_FOLDER)
            with open(f"{NAME_EMAIL_FOLDER}/{time.time()}.json", "w") as f:
                json.dump(request.form, f)
        except Exception as e:
            print(f"Exception while saving user information: {e}")
        return redirect(url_for("activity"))
    return render_template("index.html")


@app.route("/")
def consent():
    return render_template("consent.html")


@app.route("/activity")
def activity():
    if "email" not in session:
        return redirect("/")
    dialogue = next_dialogue()
    # pprint(dialogue)
    return render_template(
        "activity.html",
        MULTIWOZ_PRETTY_SLOTS=MULTIWOZ_PRETTY_SLOTS,
        STAR_PRETTY_SLOTS=STAR_PRETTY_SLOTS,
        dialogue=dialogue,
        slots=ONTOLOGIES[dialogue.dataset][dialogue.domain],
        dialogue_idx=session[DIALOGUE_IDX_KEY]
    )


@app.route("/sign_out")
def sign_out():
    session.clear()
    return redirect("/")


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


def get_last_n_lines(file_name, N):
    # Create an empty list to keep the track of last N lines
    list_of_lines = []
    # Open file for reading in binary mode
    with open(file_name, "rb") as read_obj:
        # Move the cursor to the end of the file
        read_obj.seek(0, os.SEEK_END)
        # Create a buffer to keep the last read line
        buffer = bytearray()
        # Get the current position of pointer i.e eof
        pointer_location = read_obj.tell()
        # Loop till pointer reaches the top of the file
        while pointer_location >= 0:
            # Move the file pointer to the location pointed by pointer_location
            read_obj.seek(pointer_location)
            # Shift pointer location by -1
            pointer_location = pointer_location - 1
            # read that byte / character
            new_byte = read_obj.read(1)
            # If the read byte is new line character then it means one line is read
            if new_byte == b"\n":
                # Save the line in list of lines
                list_of_lines.append(buffer.decode()[::-1])
                # If the size of list reaches N, then return the reversed list
                if len(list_of_lines) == N:
                    return list(reversed(list_of_lines))
                # Reinitialize the byte array to save next line
                buffer = bytearray()
            else:
                # If last read character is not eol then add it in buffer
                buffer.extend(new_byte)
        # As file is read completely, if there is still data in buffer, then its first line.
        if len(buffer) > 0:
            list_of_lines.append(buffer.decode()[::-1])
    # return the reversed list
    return list(reversed(list_of_lines))


@app.route("/latest_gaze_coords", methods=["POST"])
def latest_gaze_coords():
    while True:
        try:
            last_lines = get_last_n_lines(GAZE_STREAM_PATH, 5)
            for line in last_lines[::-1]:
                if line.strip() == "":
                    continue
                line = json.loads(line)
                if line["category"] == "tracker":
                    response = {"coords": line["values"]["frame"]["avg"]}
                    return jsonify(response)
        except Exception as e:
            print(e)
            print(line)
            continue


@app.route("/submit", methods=["POST"])
def telemetry():
    data = json.loads(request.data)
    if not os.path.exists(GAZE_PATH_FOLDER):
        os.mkdir(GAZE_PATH_FOLDER)
    with open(f"{session['session_id']}/{GAZE_PATH_FOLDER}/{time}.json", "w") as f:
        json.dump(data, f)
    return "success"


@click.command()
@click.argument("gaze-stream-path")
def main(gaze_stream_path):
    global GAZE_STREAM_PATH
    GAZE_STREAM_PATH = gaze_stream_path
    app.run(port=8001, debug=True)


if __name__ == "__main__":
    main()
