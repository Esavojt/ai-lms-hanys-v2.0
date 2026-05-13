import json
from pathlib import Path

INPUT_DIR = Path("./in")
OUTPUT_DIR = Path("./out")

# vytvoření output složky
OUTPUT_DIR.mkdir(exist_ok=True)

# všechny json soubory ve složce
for input_file in INPUT_DIR.glob("*.json"):

    output_file = OUTPUT_DIR / input_file.name

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            print(f"SKIP {input_file.name} -> není pole")
            continue

        converted = []

        for index, q in enumerate(data):

            converted.append({
                "id": q.get("id", index + 1),

                # kompatibilita s vaším rendererem
                "type": "choice",

                "q": q.get("q", ""),

                "opts": q.get("opts", [])
                    if isinstance(q.get("opts"), list)
                    else [],

                "ans": q.get("ans", [])
                    if isinstance(q.get("ans"), list)
                    else [],

                "pts": q.get("pts", 1.0)
                    if isinstance(q.get("pts"), (int, float))
                    else 1.0,

                "hint": q.get("hint", ""),

                "rationale": q.get("rationale", ""),

                "proc": q.get("proc", "")
            })

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(converted, f, ensure_ascii=False, indent=2)

        print(f"OK {input_file.name}")

    except Exception as e:
        print(f"ERR {input_file.name}")
        print(e)