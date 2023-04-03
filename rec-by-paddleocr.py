from recognize import recognize
from paddleocr import PaddleOCR

lang = "ch"

ocr = PaddleOCR(
    lang=lang,
    show_log=False,
)  # type: ignore


def rec(img: str):
    result = ocr.ocr(img, cls=False)
    if len(result) == 0 or len(result[0]) == 0:
        return ""
    txts = [line[1][0] for line in result[0]]
    return ", ".join(txts)


recognize(lambda img: rec(img))

