import json
from pathlib import Path
from typing import List, Text, Dict
from dataclasses import dataclass


MULTIWOZ_DOMAINS = ["hospital", "hotel", "restaurant", "attraction"]
STAR_DOMAINS = ["apartment", "bank", "hotel", "movie", "plane", "ride"]

PRETTY_SLOT_NAMES = {}


@dataclass
class Dialogue:
    id_: Text
    dataset: Text
    domain: Text
    turns: List["Utterance"]


@dataclass
class Utterance:
    text: Text
    speaker: Text


@dataclass
class Slot:
    dataset: Text
    domain: Text
    slot_name: Text
    possible_values: List[Text] = None

    def __post_init__(self):
        # TODO Normalize slot values for common domains in STAR and MULTIWOZ?
        pass


def load_multiwoz() -> List[Dialogue]:
    logs = json.load(open("datasets/MULTIWOZ2.4/MULTIWOZ2.4/data.json", "r"))
    dialogues = []
    for id_, log in logs.items():
        # System utterances have the "police" key. So I'm using that as a proxy to determine
        # whether the turn is a system turn or not.
        turns = [
            Utterance(
                turn["text"], "system" if "police" in turn["metadata"] else "user"
            )
            for turn in log["log"]
        ]

        # Filter out only single-domain dialogues.
        dialogue_domain = None
        dialogue_domains_count = 0
        for domain, goal in log["goal"].items():
            if goal:
                dialogue_domains_count += 1
                dialogue_domain = domain
                break

        if (
            len(turns) > 0
            and dialogue_domains_count == 1
            and dialogue_domain in MULTIWOZ_DOMAINS
        ):
            dialogues.append(
                Dialogue(
                    id_=id_, dataset="MULTIWOZ", domain=dialogue_domain, turns=turns
                )
            )
    return dialogues


def load_star() -> List[Dialogue]:
    dialogues = []
    for file in Path("datasets/schema_attention_model/STAR/dialogues/").glob("*.json"):
        with open(file, "r") as f:
            log = json.load(f)
            events = log["Events"]
            turns = []
            for event in events:
                if event["Agent"] == "User" and event["Action"] == "utter":
                    turns.append(Utterance(event["Text"], "user"))
                elif (
                    event["Agent"] == "Wizard" and event["Action"] == "pick_suggestion"
                ):
                    turns.append(Utterance(event["Text"], "system"))

            dialogue_domains = log["Scenario"]["Domains"]
            # Filter out only single-domain dialogues.
            if (
                len(turns) > 0
                and len(dialogue_domains) == 1
                and dialogue_domains[0] in STAR_DOMAINS
            ):
                dialogues.append(
                    Dialogue(
                        id_=log["DialogueID"],
                        dataset="STAR",
                        domain=dialogue_domains[0],
                        turns=turns,
                    )
                )
    return dialogues


def load_multiwoz_ontology() -> Dict[Text, List[Slot]]:
    slots = dict()
    ontology = json.load(open("datasets/MULTIWOZ2.4/MULTIWOZ2.4/ontology.json", "r"))
    for slot_name, possible_values in ontology.items():
        domain, slot_name = slot_name.split("-")
        slots[domain] = slots.get(domain, []) + [
            Slot(
                dataset="MULTIWOZ",
                domain=domain,
                slot_name=slot_name,
                possible_values=possible_values,
            )
        ]
    return slots


def load_star_ontology() -> Dict[Text, List[Slot]]:
    slots = dict()
    for ontology_file in Path("datasets/schema_attention_model/STAR/apis/dbs/").glob(
        "*.json"
    ):
        domain = ontology_file.stem
        ontology = json.load(open(ontology_file, "r"))
        slots[domain] = [
            Slot(
                dataset="STAR",
                domain=domain,
                slot_name=slot["Name"],
                possible_values=slot.get("Categories", None),
            )
            for slot in ontology
        ]
    return slots
