
import ollama
import json
import csv
import time

from pathlib import Path
from datetime import datetime, timezone

# ==========================================
# RESEARCH CONFIGURATION
# ==========================================

MODEL = "qwen3:8b"

TEMPERATURE = 0
SEED = 42

OUTPUT_FOLDER = Path("research_output")

JSON_FILE = OUTPUT_FOLDER / "research_log.jsonl"
CSV_FILE = OUTPUT_FOLDER / "research_log.csv"

# Create output folder if it does not exist
OUTPUT_FOLDER.mkdir(exist_ok=True)

# ==========================================
# RESEARCH INTERFACE
# ==========================================

print("=" * 55)
print("       LOCAL AI UNIVERSITY RESEARCH SYSTEM")
print("=" * 55)

print(f"Model: {MODEL}")
print(f"Temperature: {TEMPERATURE}")
print(f"Seed: {SEED}")

print("\nAll prompts and responses will be recorded.")
print("Type 'exit' to close the research session.")

print("=" * 55)

# ==========================================
# MAIN INTERACTION LOOP
# ==========================================

while True:

    prompt = input("\nRESEARCH PROMPT: ").strip()

    if prompt.lower() == "exit":
        print("\nResearch session finished.")
        break

    if not prompt:
        continue

    try:

        print("\nGenerating response...\n")

        start_time = time.perf_counter()

        # Each prompt is an independent experiment
        response = ollama.chat(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": TEMPERATURE,
                "seed": SEED
            }
        )

        elapsed_time = time.perf_counter() - start_time

        answer = response.message.content

        print("-" * 55)
        print("AI RESPONSE:")
        print("-" * 55)
        print(answer)
        print("-" * 55)

        # ==================================
        # CREATE RESEARCH RECORD
        # ==================================

        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model": MODEL,
            "temperature": TEMPERATURE,
            "seed": SEED,
            "prompt": prompt,
            "response": answer,
            "response_time_seconds": round(elapsed_time, 3)
        }

        # ==================================
        # SAVE JSONL RECORD
        # ==================================

        with open(
            JSON_FILE,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )

        # ==================================
        # SAVE CSV RECORD
        # ==================================

        fields = list(record.keys())

        file_exists = CSV_FILE.exists()

        with open(
            CSV_FILE,
            "a",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fields
            )

            if not file_exists:
                writer.writeheader()

            writer.writerow(record)

        print("\n[SUCCESS] Research record saved.")
        print(f"Response time: {elapsed_time:.2f} seconds")

    except Exception as error:

        print("\nERROR: Could not complete the request.")
        print(error)

print("\nYour research files are stored in:")
print(OUTPUT_FOLDER.resolve())
