from dataclasses import dataclass
from pathlib import Path
import json
import random
from typing import List
from dataclasses import dataclass
from flask import Flask, render_template, session


app = Flask(__name__)
app.secret_key = "TERRRIGDENOINDEdfnfw3"


MULTIWOZ_DOMAINS = []
STAR_DOMAINS = []


@dataclass
class Dialogue:
    turns: List["Utterance"]


@dataclass
class Utterance:
    text: str
    speaker: str


def load_multiwoz():
    logs = json.load(open("MULTIWOZ2.4/MULTIWOZ2.4/data.json", "r"))
    logs = list(logs.values())
    dialogues = []
    for log in logs:
        turns = [
            Utterance(
                turn["text"], "system" if "police" in turn["metadata"] else "user"
            )
            for turn in log["log"]
        ]
        dialogues.append(Dialogue(turns))
    return dialogues


def load_star():
    dialogues = []
    for file in Path("schema_attention_model/STAR/dialogues/").glob("*.json"):
        with open(file, "r") as f:
            log = json.load(f)
            events = log["events"]
            turns = []
            for event in events:
                if event["Agent"] == "User":
                    turns.append(Utterance(
                        event["Text"],
                        "user"
                    ))
                elif event["Agent"] == "Wizard" and event["Action"] == "pick_suggestion":
                    turns.append(Utterance(
                        event["Text"],
                        "system"
                    ))
            dialogues.append(Dialogue(turns))
    return dialogues


MULTIWOZ = load_multiwoz()
STAR = load_star()


def next_dialogue():
    if not session.get("DIALOGUE_IDX"):
        session["DIALOGUE_IDX"] = 0
    # Randomly decide between MultiWOZ and STAR
    if True or random.random() < 0.5:
        dialogue = random.choice(MULTIWOZ)
    else:
        dialogue = random.choice(STAR)
    session["DIALOGUE_IDX"] += 1
    return dialogue


@app.route("/")
def index():
    dialogue = next_dialogue()
    return render_template("index.html", dialogue=dialogue)


app.run(port=8001, debug=True)
