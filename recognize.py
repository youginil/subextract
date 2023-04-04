from rich.progress import track
import os
import argparse
from typing import List, Callable, Any


def frame2ts(n, d):
    ms = d / 2 + (n - 1) * d
    h = int(ms / 1000 / 3600)
    ms -= h * 3600 * 1000
    m = int(ms / 1000 / 60)
    ms -= m * 60 * 1000
    s = int(ms / 1000)
    ms -= s * 1000
    ms = int(ms)
    return (
        str(h).zfill(2)
        + ":"
        + str(m).zfill(2)
        + ":"
        + str(s).zfill(2)
        + ","
        + str(ms).zfill(3)
    )


def recognize(
    add_args: Callable[[argparse.ArgumentParser], None],
    get_args: Callable[[dict[str, Any]], None],
    rec: Callable[[str], str],
):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--img_dir", "-d", type=str, help="Sceenshot directory", required=True
    )
    parser.add_argument("--fps", type=str, help="Screenshot FPS", required=True)

    add_args(parser)

    args = vars(parser.parse_args())

    get_args(args)

    img_dir: str = args.get("img_dir")  # type: ignore
    fps: str = args.get("fps")  # type: ignore

    frame_duration = 1000 / float(fps)

    imgs: List[str] = []
    for item in filter(
        lambda x: x[0] != "." and str(x).endswith(".png"), os.listdir(img_dir)
    ):
        imgs.append(item)
    imgs.sort()

    subs: List[tuple[List[int], str]] = []

    for i in track(range(len(imgs))):
        file = os.path.join(img_dir, imgs[i])
        sentence = rec(file)
        print(imgs[i], sentence)
        if len(sentence) == 0:
            continue
        id = int(os.path.splitext(imgs[i])[0])
        if len(subs) > 0 and subs[-1][1] == sentence:
            subs[-1][0].append(id)
        else:
            subs.append(([id], sentence))

    print(subs)

    srt_items: List[str] = []
    for i, [ids, sentence] in enumerate(subs):
        st = frame2ts(ids[0], frame_duration)
        et = frame2ts(ids[-1], frame_duration)
        srt_items.append("\n".join([str(i + 1), st + " --> " + et, sentence]))

    srt_dest = img_dir + ".srt"

    with open(srt_dest, "w") as fp:
        for item in srt_items:
            fp.write("%s\n\n" % item)

    print("Saved to {}".format(srt_dest))

