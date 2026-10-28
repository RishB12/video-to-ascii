
import sys
import time
from pathlib import Path
import argparse
import subprocess
import platform

parser = argparse.ArgumentParser(description="Play ASCII video.")
parser.add_argument("video_file", nargs="?", default="video.ascii", help="Path to the ASCII video file (default: video.ascii)")

args = parser.parse_args()
INPUT_FILE = Path(args.video_file)
def main():
    if not INPUT_FILE.exists():
        raise SystemExit("Video file not found. Please provide a valid ASCII video file.")
    data = INPUT_FILE.read_text(encoding="utf-8")
    splitter = data.split("END_METADATA")
    metadata = splitter[0].split()
    FPS = int(float(metadata[0]))
    data = splitter[1].lstrip("\n")
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
            if platform.system() == "Windows":
                pass
            else: 
                subprocess.run("clear", check=True)
    

   

if __name__ == "__main__":
    main()
