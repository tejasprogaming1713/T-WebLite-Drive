#!/usr/bin/env node
import fs from "fs";
import fetch from "node-fetch";
import FormData from "form-data";

const API_UPLOAD = "https://upload.gofile.io/uploadFile";
const API_CONTENT = "https://api.gofile.io/getContent";

async function upload(filePath){
    if(!fs.existsSync(filePath)){console.log("File not found"); return;}
    const form = new FormData();
    form.append("file", fs.createReadStream(filePath));
    const res = await fetch(API_UPLOAD,{method:"POST", body:form});
    const j = await res.json();
    if(j.status) console.log("Uploaded! File ID:", j.data.fileId,"\nDownload page:", j.data.downloadPage);
    else console.log("Upload failed:", j);
}

async function download(fileId,target){
    const res = await fetch(`${API_CONTENT}?contentId=${fileId}`);
    const j = await res.json();
    if(!j.status){console.log("Error:", j); return;}
    const link = j.data.directLinkList[0];
    const dl = await fetch(link);
    const buffer = Buffer.from(await dl.arrayBuffer());
    if(!target) target = link.split("/").pop();
    fs.writeFileSync(target,buffer);
    console.log("Downloaded to:", target);
}

const args = process.argv.slice(2);
if(args[0]=="upload") upload(args[1]);
else if(args[0]=="download") download(args[1], args[2]);
else console.log("Usage: node twd.js <upload|download> <file|fileId> [target]");
