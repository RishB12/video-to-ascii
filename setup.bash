if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed. Please install python3 to proceed."
    exit 1
fi
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "Setup complete. You can now run 'bash video-to-ascii.bash' to start the process."