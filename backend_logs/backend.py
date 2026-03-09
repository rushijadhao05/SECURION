import csv
import os
from datetime import datetime

CSV_FILE = "log.csv"
TXT_FILE = "log.txt"
CSV_HEADER = ["Time", "CameraID", "PersonID", "MatchScore", "MatchResult", "Risk", "Event"]


def ensure_files():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADER)

    if not os.path.exists(TXT_FILE):
        with open(TXT_FILE, "w", encoding="utf-8") as f:
            f.write("===== HUMAN READABLE SECURITY LOGS =====\n\n")


def decide_risk(result, score):
    if result == "Unknown":
        return "High", "Alert"
    elif score < 0.70:
        return "Medium", "Suspicious"
    else:
        return "Low", "Detected"


def write_csv(row):
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(row)


def write_txt(row):
    time, camera_id, person_id, score, result, risk, event = row
    line = (
        f"[{time}] | Camera: {camera_id} | Person: {person_id} | "
        f"Score: {score} | Result: {result} | Risk: {risk} | Event: {event}\n"
    )
    with open(TXT_FILE, "a", encoding="utf-8") as f:
        f.write(line)


def simulate_event(i):
    return {
        "camera_id": "cam_01",
        "person_id": f"om{i % 3}",
        "score": round(0.55 + (i % 5) * 0.1, 2),
        "result": "Matched" if i % 4 != 0 else "Unknown"
    }


def show_statistics():
    total = 0
    high = 0
    medium = 0
    low = 0

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            risk = row["Risk"].strip()

            if risk == "High":
                high += 1
            elif risk == "Medium":
                medium += 1
            elif risk == "Low":
                low += 1

    print("\n===== LOG STATISTICS =====")
    print("Total Events :", total)
    print("High Risk    :", high)
    print("Medium Risk  :", medium)
    print("Low Risk     :", low)


if __name__ == "__main__":
    print("===== SECURION FINAL BACKEND =====")

    ensure_files()

    for i in range(10):
        data = simulate_event(i)

        risk, event = decide_risk(data["result"], data["score"])

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        row = [
            current_time,
            data["camera_id"],
            data["person_id"],
            data["score"],
            data["result"],
            risk,
            event
        ]

        write_csv(row)
        write_txt(row)

        print("Logged:", row)

    print("\nLogs saved successfully.")
    print("CSV File:", CSV_FILE)
    print("TXT File:", TXT_FILE)

    show_statistics()
