extract_frames() {
    read -p "Enter video filename: " videopath 
    read -p "Enter fps (frames per second): " fps
    read -p "Enter scale width (height will be auto-scaled): " scale_width
    read -p "Proceeding will delete the 'frames' directory if it exists. Do you want to continue? (y/n): " confirm
    if [[ "$confirm" =~ ^[yY]$ ]]; then
        echo "Operation cancelled."
        exit 1
    fi
    if [ ! -f "$videopath" ]; then
        echo "Error: File '$videopath' not found!"
        exit 1
    fi
    if ! [[ "$fps" =~ ^[0-9]+$ ]]; then
        echo "Error: FPS must be a positive integer."
        exit 1
    fi
    if ! [[ "$scale_width" =~ ^[0-9]+$ ]]; then
        echo "Error: Scale width must be a positive integer."
        exit 1
    fi
    if ! command -v ffmpeg &> /dev/null; then
        echo "Error: ffmpeg is not installed. Please install ffmpeg to proceed."
        exit 1
    fi
    rm -rf frames
    mkdir frames
    ffmpeg -i "$videopath" -vf "fps=$fps,scale=$scale_width:-1:flags=lanczos,format=gray" frames/%06d.png
}

source .venv/bin/activate
extract_frames
python convert.py
python play.py