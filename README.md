# video-to-ascii

Turn a video into a terminal-based ASCII animation.

This project extracts frames from a video, converts each frame into grayscale ASCII, saves them to a text file, and replays the result in the terminal as an animated sequence.

## How it works

The workflow is split into three stages:

1. Extract frames from the source video using `ffmpeg`.
   - The script `video-to-ascii.bash` prompts for:
     - the input video path
     - the target FPS
     - the output width for the ASCII rendering
   - ffmpeg then writes each frame to `frames/` as numbered PNG files.

2. Convert frames into ASCII art with `convert.py`.
   - Each PNG is opened with Pillow.
   - The image is converted to grayscale.
   - It is resized to a chosen terminal-friendly width.
   - Every pixel brightness value is mapped to a character from a predefined ASCII ramp:

     ```python
     CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"\^\`'."
     ```

   - Dark pixels become characters like `.` or `,`, while bright pixels become denser symbols like `@` or `$`.
   - The result is written to `video.ascii`, with form-feed characters (`\f`) separating individual frames.

3. Replay the animation in the terminal with `play.py`.
   - `play.py` reads `video.ascii` and splits it into frames.
   - It clears the terminal and prints each frame in sequence.
   - It uses ANSI escape codes to move the cursor to the top-left and clear the screen before each refresh.
   - The playback rate is controlled by `FPS` in the script.

In short, the project turns light/dark values in a video into text characters and displays them sequentially so the output looks like a moving ASCII film in a terminal.

## Requirements

Before running the project, make sure you have:

- Python 3
- `ffmpeg` installed and available on your PATH
- The Python packages in `requirements.txt`
- A terminal with enough width to display the ASCII output cleanly

### Python dependencies

The project uses:

- `pillow` for image processing
- `tqdm` for progress output

Install them with:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Installation

From the repository root:

```bash
git clone <repo-url>
cd "Video to Ascii"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If you prefer the project helper script, you can also run:

```bash
bash setup.bash
```

This script creates the virtual environment and installs the required dependencies.

## Usage

### Quick start

The easiest way to run the project is:

```bash
bash video-to-ascii.bash
```

The script will ask for:

- the input video file path
- the FPS value to extract (15 is recommended)
- the ASCII width for the output (120 is recommended)

Then it will:

1. create the `frames/` directory
2. extract frames with `ffmpeg`
3. convert the frames to ASCII with `convert.py`
4. play the result in the terminal with `play.py`

### Manual workflow

If you want to run each step yourself:

1. Extract frames:

   ```bash
   ffmpeg -i input.mp4 -vf "fps=15,scale=120:-1:flags=lanczos,format=gray" frames/%06d.png
   ```

2. Convert frames to ASCII:

   ```bash
   python3 convert.py
   ```

3. Play the animation:

   ```bash
   python3 play.py
   ```

### Files created by the project

- `frames/` — extracted PNG frames
- `video.ascii` — the generated ASCII animation file

## Configuration

You can adjust these values in the scripts:

- `FPS` in `play.py` controls playback speed.
- `WIDTH` in `convert.py` controls the horizontal resolution of the ASCII output.
- `CHAR_ASPECT` in `convert.py` helps preserve the proportions of the rendered characters.
- `CHARS` in `convert.py` changes the brightness mapping used for ASCII conversion.

## Tips

- Use a video with good contrast for better-looking output.
- Start with short clips while testing.
- If the output is too wide or too tall, reduce the width value.
- Try different FPS values to get smoother or slower playback.
- Use a larger terminal window for a more detailed ASCII image.

## Troubleshooting

### `ffmpeg` is not found

Install ffmpeg:

```bash
sudo apt update
sudo apt install ffmpeg
```

### `video.ascii not found`

Run:

```bash
python3 convert.py
```

before starting playback.

### The ASCII output is too compressed or too wide

Lower or raise the width parameter in `video-to-ascii.bash` or the `WIDTH` value in `convert.py`.

### The project cannot find the video

Check that the path is correct and that the file exists before running the script.

### Terminal output is messy

Use a monospaced terminal and make sure the font supports the characters used in the output.

## Contributing

Contributions are welcome. If you find a bug or want to improve the project, open an issue or submit a pull request with a clear description of the change.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---