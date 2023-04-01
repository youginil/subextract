import math
import os
import argparse

parser = argparse.ArgumentParser(description='Extract video frames')
parser.add_argument('--input', '-i', type=str,
                    help='Video path', required=True)
parser.add_argument('--output', '-o', type=str,
                    help='Output directory', required=True)
parser.add_argument('--fps', type=float, help='Frames per second', default=10)
parser.add_argument('--crop', type=int, nargs='+',
                    help='Crop params. --crop width height x y or --crop x y')

args = vars(parser.parse_args())
video = args.get('input')
if not os.path.isfile(video):
    raise ValueError("Invalid video path")
dest = args.get('output')
if os.path.exists(dest):
    if os.path.isdir(dest):
        if len(os.listdir(dest)) > 0:
            raise ValueError('The output directory is NOT EMPTY')
    else:
        os.makedirs(dest)
else:
    os.makedirs(dest)
fps = args.get('fps')

output = os.popen(
    'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {}'.format(video))
duration = output.read()
duration = float(duration)

total = math.ceil(duration * fps)
max_length = len(str(total))
crop = args.get('crop')
crop_filter = ''
if crop is not None:
    if len(crop) != 2 and len(crop) != 4:
        raise ValueError("Invalid crop")
    else:
        crop_filter = 'crop=' + ':'.join(map(lambda x: str(x), crop))
fps_filter = 'fps={}'.format(fps)
filter = ', '.join(filter(lambda x: len(x) > 0, [crop_filter, fps_filter]))

cmd = 'ffmpeg -i {} -vf "{}" {}{}%0{}d.png'.format(
    video, filter, dest, os.path.sep, max_length)
print(cmd)
os.system(cmd)
