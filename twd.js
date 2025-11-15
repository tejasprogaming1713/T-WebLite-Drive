#!/usr/bin/env node

import fs from "fs";
import FormData from "form-data";
import fetch from "node-fetch";

const API_UPLOAD = "https://upload.gofile.io/uploadFile";
const API_CONTENT = "https://api.gofile.io/getContent";

async function upload(filePath, token) {
  if (!fs.existsSync(filePath)) {
    console.error("File does not exist:", filePath);
    process.exit(1);
  }
  const form = new FormData();
  form.append("file", fs.createReadStream(filePath));
  if (token) form.append("token", token);

  const res = await fetch(API_UPLOAD, { method: "POST", body: form });
  const data = await res.json();
  if (data.status) {
    console.log("Uploaded! File ID:", data.data.fileId);
    console.log("Download Page:", data.data.downloadPage);
  } else {
    console.error("Upload failed:", data);
  }
}

async function download(fileId, target) {
  const url = `${API_CONTENT}?contentId=${fileId}`;
  const res = await fetch(url);
  const j = await res.json();
  if (!j.status) {
    console.error("Error:", j);
    return;
  }
  const link = j.data.directLinkList[0];
  const fileRes = await fetch(link);
  const arrayBuffer = await fileRes.arrayBuffer();
  const buffer = Buffer.from(arrayBuffer);
  const filename = target || link.split("/").pop();
  fs.writeFileSync(filename, buffer);
  console.log("Downloaded to:", filename);
}

function usage() {
  console.log("Usage: twd <command> [args]");
  console.log("Commands:");
  console.log("  upload <file_path> [token]");
  console.log("  download <file_id> [target]");
}

async function main() {
  const args = process.argv.slice(2);
  const cmd = args[0];
  if (cmd === "upload") {
    await upload(args[1], args[2]);
  } else if (cmd === "download") {
    await download(args[1], args[2]);
  } else {
    usage();
  }
}

main();
