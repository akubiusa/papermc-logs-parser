import hashlib
import json
import os
import sys

from src import parser


def main():
    if not os.path.exists("./config.json"):
        print("[ERROR] config.json not found.")
        sys.exit(1)

    with open("./config.json", "r") as f:
        config = json.load(f)

    data = {}
    if os.path.exists("./data.json"):
        with open("./data.json", "r") as f:
            data = json.load(f)

    if not os.path.exists(config["path"]):
        parser(config["path"])

    with open(config["path"], "rb") as f:
        initial_stat = os.fstat(f.fileno())
        initial_content = f.read()

    logs = parser(config["path"])

    with open("./output.json", "w") as f:
        json.dump(logs, f)

    dataCount = len(logs)
    firstTime = logs[0]["time"] if logs else None
    with open(config["path"], "rb") as f:
        stat = os.fstat(f.fileno())
        content = f.read()

    source = {
        "path": os.path.realpath(config["path"]),
        "device": stat.st_dev,
        "inode": stat.st_ino,
    }
    stable = (initial_stat.st_dev, initial_stat.st_ino) == (
        stat.st_dev,
        stat.st_ino,
    ) and initial_content == content
    previous_size = data.get("size")
    previous_count = data.get("count")
    valid_cursor = all(
        [
            stable,
            data.get("source") == source,
            isinstance(previous_size, int),
            isinstance(previous_count, int),
        ]
    )
    if valid_cursor:
        valid_cursor = (
            0 <= previous_size <= len(content) and 0 <= previous_count <= dataCount
        )
    if valid_cursor:
        digest = hashlib.sha256(content[:previous_size]).hexdigest()
        if digest == data.get("digest"):
            logs = logs[previous_count:]

    print(logs)

    with open("./data.json", "w") as f:
        json.dump(
            {
                "count": dataCount,
                "firstTime": firstTime,
                "source": source if stable else None,
                "size": len(content),
                "digest": hashlib.sha256(content).hexdigest(),
            },
            f,
        )


if __name__ == "__main__":
    main()
