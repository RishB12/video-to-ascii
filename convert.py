from pathlib import Path
from PIL import Image
from tqdm import tqdm

FRAMES_DIR = Path("frames")
OUTPUT_FILE = Path("video.ascii")

# Darkest to brightest
CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"\^\`\'."

WIDTH = 120
CHAR_ASPECT = 0.5  # Approximate character width / height


def image_to_ascii(path):
    with Image.open(path) as image:
        image = image.convert("L")

        height = round(
            image.height * WIDTH / image.width * CHAR_ASPECT
        )

        image = image.resize((WIDTH, max(1, height)))
        pixels = list(image.getdata())

    result = []

    for y in range(height):
        row = []

        for x in range(WIDTH):
            brightness = pixels[y * WIDTH + x]
            index = brightness * (len(CHARS) - 1) // 255
            row.append(CHARS[index])

        result.append("".join(row))

    return "\n".join(result)


def main():
    frames = sorted(FRAMES_DIR.glob("*.png"))

    if not frames:
        raise SystemExit("No PNG frames found in frames/")

    with OUTPUT_FILE.open("w", encoding="utf-8") as output:
        for number, frame in enumerate(tqdm(frames, desc="Converting frames"), 1):
            ascii_frame = image_to_ascii(frame)

            # Form-feed separates frames in the output file.
            if number > 1:
                output.write("\f")

            output.write(ascii_frame)

    print(f"Done! Saved {len(frames)} frames to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()