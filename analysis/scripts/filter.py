import json
import re
import click


with open("../../datasets/MULTIWOZ2.4/MULTIWOZ2.4/data.json", "r") as f:
    data = json.load(f) 


def main():
    global data
    queries = []
    while True:
        query = input("Query: ").lower()
        # Recognize up arrow
        if query.strip() == "^[[a":
            query = queries[-1]
            print(query)
        else:
            queries.append(query)
        if ">" not in query:
            constraints, max_turns = query, None
        else:
            constraints, max_turns = query.split(">")
        candidates = []
        for dialogue_id, log in data.items():
            goal = json.dumps(log["log"]).lower()
            for q in constraints.split(","):
                if q not in goal:
                    break
                if max_turns is not None and len(log["log"]) < int(max_turns):
                    break
            else:
                candidates.append(dialogue_id)
            continue
        print(candidates)

if __name__ == '__main__':
    main()