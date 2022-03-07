import json
from pathlib import Path
from typing import List, Text
from dataclasses import dataclass


MULTIWOZ_DOMAINS = []
STAR_DOMAINS = []


@dataclass
class Dialogue:
    turns: List["Utterance"]


@dataclass
class Utterance:
    text: Text
    speaker: Text


def load_multiwoz():
    logs = json.load(open("datasets/MULTIWOZ2.4/MULTIWOZ2.4/data.json", "r"))
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
    for file in Path("datasets/schema_attention_model/STAR/dialogues/").glob("*.json"):
        with open(file, "r") as f:
            log = json.load(f)
            events = log["Events"]
            turns = []
            for event in events:
                if event["Agent"] == "User" and event["Action"] == "utter":
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


