import { program } from "commander";
import fs from "fs/promises";
import { exec } from "child_process";
import path from "path";
import cliProgress from "cli-progress";

function frame2ts(n, d) {
  let ms = d / 2 + (n - 1) * d;
  const h = Math.floor(ms / 1000 / 3600);
  ms -= h * 3600 * 1000;
  const m = Math.floor(ms / 1000 / 60);
  ms -= m * 60 * 1000;
  const s = Math.floor(ms / 1000);
  ms -= s * 1000;
  return (
    `${h}`.padStart(2, "0") +
    ":" +
    `${m}`.padStart(2, "0") +
    ":" +
    `${s}`.padStart(2, "0") +
    "," +
    `${ms}`.padStart(3, "0")
  );
}

function execCommand(cmd) {
  return new Promise((resolve, reject) => {
    exec(cmd, (err, stdout, stderr) => {
      if (err) {
        reject(err);
      } else {
        resolve({
          stdout,
          stderr,
        });
      }
    });
  });
}

program
  .requiredOption("-d, --img_dir <string>", "Screenshot directory")
  .requiredOption("--fps <string>", "Screenshot FPS");

export default async function recognize(rec) {
  program.parse();
  const options = program.opts();
  const fps = +options.fps;
  if (isNaN(fps) || fps <= 0) {
    throw new Error("Invalid FPS");
  }
  const imgDir = options.img_dir;
  if (!(await fs.stat(imgDir)).isDirectory()) {
    throw new Error("Invalid image directory");
  }

  const imgs = (await fs.readdir(imgDir))
    .filter((item) => item.endsWith(".png"))
    .sort((a, b) => a - b);

  const subs = [];
  for (let i = 0; i < imgs.length; i++) {
    const img = imgs[i];
    const file = path.resolve(imgDir, imgs[i]);
    const sentence = await rec(file);
    console.log(img + "/" + imgs.length, sentence);
    if (sentence === "") {
      continue;
    }
    const id = +img.substring(0, img.length - path.extname(img).length);
    if (subs.length > 0 && subs[subs.length - 1].sentence === sentence) {
      subs[subs.length - 1].ids.push(id);
    } else {
      subs.push({
        ids: [id],
        sentence,
      });
    }
  }

  const frame_duration = 1000 / fps;

  const sub_items = [];
  subs.forEach(({ ids, sentence }, idx) => {
    const st = frame2ts(ids[0], frame_duration);
    const et = frame2ts(ids[ids.length - 1], frame_duration);
    sub_items.push(["" + idx, st + " --> " + et, sentence]);
  });

  const dest = imgDir + ".srt";

  await fs.writeFile(dest, sub_items.join("\n\n"));
  console.log(`Save to ${dest}`);
}

