
import sys
import time
from pathlib import Path

FPS = 15
INPUT_FILE = Path("video.ascii")


def main():
    if not INPUT_FILE.exists():
        raise SystemExit("video.ascii not found. Run convert.py first.")

    data = INPUT_FILE.read_text(encoding="utf-8")
    frames = data.split("\f")
    delay = 1 / FPS

    try:
        for frame in frames:
            # ANSI escape sequence: move cursor home and clear screen
            sys.stdout.write("\033[2J\033[H")
            sys.stdout.write(frame)
            sys.stdout.write("\n")
            sys.stdout.flush()

            time.sleep(delay)

    except KeyboardInterrupt:
        pass

    finally:
        # Reset terminal formatting and show the cursor
        sys.stdout.write("\033[0m\033[?25h\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
