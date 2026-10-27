extract_frames() {
    read -p "Enter video filename: " videopath 
    read -p "Enter scale width (height will be auto-scaled) (120 recommended): " scale_width
    read -p "Proceeding will delete the 'frames' directory if it exists. Do you want to continue? (y/n): " confirm

    if [[ ! "$confirm" =~ ^[yY]([eE][sS])?$ ]]; then
        echo "Operation cancelled."
        exit 1
    fi

    if [ ! -f "$videopath" ]; then
        echo "Error: File '$videopath' not found!"
        exit 1
    fi
    if ! [[ "$scale_width" =~ ^[0-9]+$ ]]; then
        echo "Error: Scale width must be a positive integer."
        exit 1
    fi
    if ! command -v ffmpeg &> /dev/null; then
        echo "Error: ffmpeg is not installed. Please install ffmpeg using 'sudo apt update && sudo apt install ffmpeg' to proceed."
        exit 1
    fi
    rm -rf frames
    mkdir frames
    
}

if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed. Please install python3 to proceed."
    exit 1
fi

source .venv/bin/activate

echo "Welcome to video-to-ascii! This script will convert a video into ASCII art and play it in the terminal."
echo "Options:"
echo "1. Convert a video to ASCII and play it"
echo "2. Play last converted video"
echo "3. Use pre-extracted frames to convert to ASCII and play it"
echo "4. Use pre-existing .ascii files to play ASCII art"
read -p "Please select an option (1, 2, 3, or 4): " option

case $option in
    1)
        extract_frames
        read -p "Do you want colorize the ASCII output? (y/n): " colorize
        if [[ "$colorize" =~ ^[yY]([eE][sS])?$ ]]; then
            python3 convert.py $videopath $scale_width -c
        else
            python3 convert.py $videopath $scale_width
        fi
        python3 play.py "video.ascii"
        ;;
    2)
        python3 play.py "video.ascii"
        ;;
    3)
        if [ ! -d "frames" ]; then
            echo "Error: 'frames' directory not found."
            exit 1
        fi
        read =p "Do you want colorize the ASCII output? (y/n): " colorize
        if [[ "$colorize" =~ ^[yY]([eE][sS])?$ ]]; then
            python3 convert.py $videopath $scale_width -c
        else
            python3 convert.py $videopath $scale_width
        fi
        python3 play.py "video.ascii"
        ;;
    4)
        read -p "Enter the .ascii filename (eg. video.ascii): " ascii_filename
        if [ ! -f "$ascii_filename" ]; then
            echo "Error: File '$ascii_filename' not found."
            exit 1
        fi
        python3 play.py "$ascii_filename"
        ;;

    *)
        echo "Invalid option. Please select 1, 2, 3, or 4."
        exit 1
        ;;
esac
