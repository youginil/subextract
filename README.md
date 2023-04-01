# subextract

Some scripts for extracting subtitle (hard-encoded) from video

## Requirements

- Python
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- ffmpeg and ffprobe

## Installation

```
pip install -r requirements.txt
```

## Usage

1. Capture screenshots

```
python screenshot.py -i {video} -o {img_dir}

# --crop should be used for capturing subtitle area only.
# more options in --help

```

2. Recognize text from screenshots and generate a subtitle file

```
python recognize.py -v {video} -d {img_dir}
# Specify the subtitle language by --lang, more information in PaddleOCR document.
```

## Post-recognization

The result maybe not accurate, you can correct it manually by subtitle editor, such as [Aegisub](https://github.com/Aegisub/Aegisub), or improve it through changing PaddleOCR models.

## TODO
- Add more options to scripts
- Add more OCR tools
