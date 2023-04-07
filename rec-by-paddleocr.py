from recognize import recognize
from paddleocr import PaddleOCR
import argparse
from typing import Any, Dict


ocr: PaddleOCR

param_keys = ["det_model_dir", "cls_model_dir", "rec_model_dir", "ocr_version"]


def add_args(parser: argparse.ArgumentParser):
    parser.add_argument("--lang", type=str, default="ch")
    for k in param_keys:
        parser.add_argument("--" + k, type=str)


def get_args(args: dict[str, Any]):
    global ocr
    params: Dict[str, Any] = {
        "show_log": False,
        "lang": args.get("lang"),
    }
    for k in param_keys:
        v = args.get(k)
        if v:
            params[k] = v

    ocr = PaddleOCR(**params)  # type: ignore


def rec(img: str):
    # todo 识别下一张图片相同的区域，如果不一致再整体识别。如果相同的区域一样，但区域外还有内容，那就识别错了
    result = ocr.ocr(img, cls=False)
    if len(result) == 0 or len(result[0]) == 0:
        return ""
    txts = [line[1][0] for line in result[0]]
    return "\n".join(txts)


recognize(add_args, get_args, rec)

