from pathlib import Path
from PIL import Image
from tqdm import tqdm
import argparse
import cv2
import subprocess

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

def get_fps(vidp):
    video = cv2.VideoCapture(vidp)
    fps = video.get(cv2.CAP_PROP_FPS)
    video.release()
    if fps <= 0:
        print("Failed to get FPS from metadata, defaulting to 60 FPS")
        return 60
    return fps

def image_to_ascii(path, colour=False):
    with Image.open(path) as image:
        image = image.convert("RGB")

        height = round(
            image.height * WIDTH / image.width * CHAR_ASPECT
        )

        image = image.resize((WIDTH, max(1, height)))
        pixels = list(image.getdata())

    result = []

    for y in range(height):
        row = []

        for x in range(WIDTH):
            r, g, b = pixels[y * WIDTH + x]
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

def main():
    FPS = get_fps(f"{args.Main_Video_File}")
    subprocess.run(["ffmpeg",
                   "-i", 
                   f"{args.Main_Video_File}",
                   "-vf",
                   f"fps={FPS},scale={args.Scale_W}:-1:flags=lanczos",
                   "frames/%06d.png"], check = True
                   )
    print("FPS =", FPS)
    frames = sorted(FRAMES_DIR.glob("*.png"))
    if not frames:
        raise SystemExit("No PNG frames found in frames/")

    with OUTPUT_FILE.open("w", encoding="utf-8") as output:
        output.write(str(FPS))
        output.write("\n")
        output.write("END_METADATA\n")
        for number, frame in enumerate(tqdm(frames, desc="Converting frames"), 1):
            ascii_frame = image_to_ascii(frame, colour=args.colour)

            # Form-feed separates frames in the output file.
            if number > 1:
                output.write("\f")

            output.write(ascii_frame)

    print(f"Done! Saved {len(frames)} frames to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()