import math
import os
import argparse
from typing import Optional

parser = argparse.ArgumentParser(description="Extract video frames")
parser.add_argument("--input", "-i", type=str, help="Video path", required=True)
parser.add_argument("--output", "-o", type=str, help="Output directory", required=True)
parser.add_argument("--fps", type=str, help="Frames per second", default="10")
parser.add_argument(
    "--crop",
    "-c",
    type=int,
    nargs="+",
    help="Crop params. --crop width height x y or --crop x y",
)
parser.add_argument("--scale", type=str, help="Image scale")

args = vars(parser.parse_args())

video: str = args.get("input")  # type: ignore
if not os.path.isfile(video):
    raise ValueError("Invalid video path")

dest: str = args.get("output")  # type: ignore
if os.path.exists(dest):
    if os.path.isdir(dest):
        if len(os.listdir(dest)) > 0:
            raise ValueError("The output directory is NOT EMPTY")
    else:
        os.makedirs(dest)
else:
    os.makedirs(dest)

fps: str = args.get("fps")  # type: ignore
fps_value = float(fps)

output = os.popen(
    "ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {}".format(
        video
    )
)
duration = output.read()
duration = float(duration)

total = math.ceil(duration * fps_value)
max_length = len(str(total))

crop = args.get("crop")
crop_filter = ""
if crop is not None:
    if len(crop) != 2 and len(crop) != 4:
        raise ValueError("Invalid crop")
    else:
        crop_filter = "crop=" + ":".join(map(lambda x: str(x), crop))
fps_filter = "fps={}".format(fps)

scale: Optional[str] = args.get("scale")
scale_filter = ""
if scale :
    scale_filter = "scale=" + scale

filter = ", ".join(
    filter(lambda x: len(x) > 0, [crop_filter, fps_filter, scale_filter])
)

cmd = 'ffmpeg -i {} -vf "{}" {}{}%0{}d.png'.format(
    video, filter, dest, os.path.sep, max_length
)
print(cmd)
os.system(cmd)

