import { createWorker } from "tesseract.js";
import recognize from "./recognize.mjs";

await (async () => {
  const worker = await createWorker({
    cachePath: "",
  });
  await worker.loadLanguage("chi_tra");
  await worker.initialize("chi_tra");

  await recognize(async (img) => {
    const {
      data: { text },
    } = await worker.recognize(img);
    return text;
  });

  await worker.terminate();
})();
