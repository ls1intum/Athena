import type { NextApiRequest, NextApiResponse } from "next";
import fs from "fs";
import path from "path";
import formidable from "formidable";
import unzipper from "unzipper";

export const config = {
  api: {
    bodyParser: false,
  },
};

const UPLOAD_DIR = path.join(process.cwd(), "data/evaluation");

async function handleFileUpload(file: formidable.File, directory: string) {
  const filePath = path.join(directory, file.originalFilename || file.newFilename);

  if (file.mimetype === "application/zip") {
    await new Promise((resolve, reject) => {
      fs.createReadStream(file.filepath)
        .pipe(unzipper.Extract({ path: directory }))
        .on("close", resolve)
        .on("error", reject);
    });
  } else if (file.mimetype === "application/json") {
    fs.copyFileSync(file.filepath, filePath);
  } else {
    throw new Error("Unsupported file type");
  }
}

async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (!req.query.dataMode?.toString().startsWith("evaluation-")) {
    return res.status(400).json({ error: "Invalid data mode" });
  }

  const form = new formidable.IncomingForm();
  const dataMode = req.query.dataMode as string;
  const customDir = dataMode.slice(dataMode.indexOf("-") + 1)
  const directory = path.join(UPLOAD_DIR, customDir);

  if (!fs.existsSync(directory)) {
    fs.mkdirSync(directory, { recursive: true });
  }

  form.parse(req, async (err, fields, files) => {
    if (err) {
      return res.status(500).json({ error: "Failed to parse form data" });
    }

    try {
      const fileArray = (Array.isArray(files.file) ? files.file : [files.file]).filter((file) => file !== undefined);

      for (const file of fileArray) {
        await handleFileUpload(file, directory);
      }

      res.status(200).json({ success: true });
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: "Failed to handle file upload" });
    }
  });
}

export default handler;
