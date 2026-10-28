from pathlib import Path
from time import time
from PIL import Image
import argparse
import cv2
import subprocess
import time
import json
import sys
import shutil

parser = argparse.ArgumentParser(description="Convert video frames to ASCII art")

parser.add_argument(
    "-c", "--colour", "--color",
    dest="colour",
    action="store_true",
    help="Enable RGB colour output"
)
parser.add_argument(
    "Main_Video_File",
    help="Main video file for FPS"
)
parser.add_argument(
    "Scale_W",
    help="Scale Width"
)
args = parser.parse_args()

FRAMES_DIR = Path("frames")
OUTPUT_FILE = Path("video.ascii")

# Darkest to brightest
CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"\^\`\'."[::-1]

WIDTH = int(args.Scale_W)
CHAR_ASPECT = 0.5  # Approximate character width / height
TIMES = []

def get_fps(vidp):
    video = cv2.VideoCapture(vidp)
    fps = video.get(cv2.CAP_PROP_FPS)
    video.release()
    if fps <= 0:
        print("Failed to get FPS from metadata, defaulting to 60 FPS")
        return 60
    return fps

def image_to_ascii_image(image, colour=False):
    image = image.convert("RGB")

    colums, lines = shutil.get_terminal_size()

    twidth = max(1, colums-1)
    max_height = max(1, lines-1)

    height = min(max_height, round(image.height * twidth / image.width * CHAR_ASPECT))

    image = image.resize((twidth, height))
    pixels = list(image.get_flattened_data())

    result = []

    for y in range(height):
        row = []

        for x in range(twidth):
            r, g, b = pixels[y * twidth + x]
            brightness = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
            index = brightness * (len(CHARS) - 1) // 255
            char = CHARS[index]

            if colour:
                row.append(f"\033[38;2;{r};{g};{b}m{char}")
            else:
                row.append(char)

        if colour:
            result.append("".join(row) + "\033[0m")
        else:
            result.append("".join(row))
    return "\n".join(result)

def image_to_ascii(path, colour=False):
    with Image.open(path) as image:
        return image_to_ascii_image(image, colour)

def stream_video(video_path, width=WIDTH, colour=True):
    # Ask FFprobe for the video's original dimensions.
    probe = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height",
            "-of", "json", str(video_path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    stream = json.loads(probe.stdout)["streams"][0]
    source_width = stream["width"]
    source_height = stream["height"]

    # Preserve aspect ratio and use an even output height.
    height = max(
        2,
        round((source_height * width / source_width) / 2) * 2,
    )

    fps = get_fps(video_path)  
    #frame_size = width * height * 3  # RGB = 3 bytes per pixel

    command = [
        "ffmpeg", "-v", "error",
        "-i", str(video_path),
        "-vf", f"fps={fps},scale={width}:{height}:flags=lanczos",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "pipe:1",
    ]

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )

    frame_interval = 1 / fps
    next_frame = time.monotonic()

    try:
        # Clear the terminal once, then redraw at the cursor position.
        sys.stdout.write("\033[2J")
        sys.stdout.flush()

        while True:

            frame_size = width * height * 3  # RGB = 3 bytes per pixel
            data = process.stdout.read(frame_size)

            if not data:
                break

            if len(data) != frame_size:
                raise RuntimeError("Received an incomplete video frame")

            image = Image.frombytes(
                "RGB", (width, height), data
            )

            ascii_frame = image_to_ascii_image(
                image, colour=colour
            )

            sys.stdout.write("\033[H" + ascii_frame)
            sys.stdout.flush()

            # Pace playback instead of printing as fast as possible.
            next_frame += frame_interval
            delay = next_frame - time.monotonic()

            if delay > 0:
                time.sleep(delay)
    except KeyboardInterrupt:
        print("\nPlayback interrupted by user.", file=sys.stderr)
    else:
        return_code = process.wait()
        if return_code != 0:
            raise RuntimeError(
                f"FFmpeg exited with code {return_code}"
            )
        print("\nPlayback finished.")


    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=0.5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        if process.stdout is not None:
            process.stdout.close()
        sys.stdout.write("\033[0m")  # Reset terminal formatting
        sys.stdout.flush()

def main():
    stream_video(args.Main_Video_File, colour=args.colour)


if __name__ == "__main__":
    main()