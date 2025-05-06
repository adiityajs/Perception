from pathlib import Path
import sys

# Get the absolute path of the current file
FILE = Path(__file__).resolve()
# Get the parent directory of the current file
ROOT = FILE.parent
# Add the root path to the sys.path list if it is not already there
if ROOT not in sys.path:
    sys.path.append(str(ROOT))
# Get the relative path of the root directory with respect to the current working directory
ROOT = ROOT.relative_to(Path.cwd())

# Sources
IMAGE = 'Image'
VIDEO = 'Video'
WEBCAM = 'Webcam'
YOUTUBE = 'YouTube'

SOURCES_LIST = [IMAGE, VIDEO, WEBCAM,   YOUTUBE]

# Images config
IMAGES_DIR = ROOT / 'images'
DEFAULT_IMAGE = IMAGES_DIR / 'sample object detection.png'

# Videos config
VIDEO_DIR = ROOT / 'videos'
VIDEOS_DICT = {
    'v1': VIDEO_DIR / 'v1.mp4',
    'v2': VIDEO_DIR / 'v2.mp4',
    'v3': VIDEO_DIR / 'v3.mp4',
    'v4': VIDEO_DIR / 'v4.mp4',
    'v5': VIDEO_DIR / 'v5.mp4',
    'v6': VIDEO_DIR / 'v6.mp4',
    'v7': VIDEO_DIR / 'v7.mp4',
}

# ML Model config
MODEL_DIR = ROOT / 'weights'
DETECTION_MODEL = MODEL_DIR / 'yolov8n.pt'
# In case of your custome model comment out the line above and
# Place your custom model pt file name at the line below 
# DETECTION_MODEL = MODEL_DIR / 'my_detection_model.pt'


# Webcam
WEBCAM_PATH = 0
