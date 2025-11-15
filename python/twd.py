#!/usr/bin/env python3

import sys
import os
import requests

# =============== GoFile.io API ===============
# Upload endpoint: https://upload.gofile.io/uploadFile 1

def upload(file_path, token=None):
    if not os.path.exists(file_path):
        print("Error: File does not exist:", file_path)
        return
    url = "https://upload.gofile.io/uploadFile"
    files = {"file": open(file_path, "rb")}
    data = {}
    if token:
        data["token"] = token
    resp = requests.post(url, files=files, data=data)
    result = resp.json()
    if result["status"]:
        file_id = result["data"]["fileId"]
        download_page = result["data"]["downloadPage"]
        print("Uploaded! File ID:", file_id)
        print("Download page:", download_page)
    else:
        print("Upload failed:", result)

def download(file_id, target=None):
    # We need to get a direct link from GoFile content API
    api = f"https://api.gofile.io/getContent?contentId={file_id}"
    resp = requests.get(api)
    result = resp.json()
    if not result["status"]:
        print("Error:", result)
        return
    # Pick the first direct link
    links = result["data"]["directLinkList"]
    if not links:
        print("No download link found.")
        return
    link = links[0]
    if not target:
        target = link.split("/")[-1]
    dl = requests.get(link, stream=True)
    with open(target, "wb") as f:
        for chunk in dl.iter_content(chunk_size=8192):
            f.write(chunk)
    print("Downloaded to:", target)

def delete(content_id, token):
    # Delete only works if you have a token and the content belongs to you
    api = "https://api.gofile.io/contents"
    headers = {"Content-Type": "application/json"}
    data = {
        "contentsId": content_id
    }
    if token:
        data["token"] = token
    resp = requests.delete(api, json=data, headers=headers)
    result = resp.json()
    print("Delete response:", result)

def usage():
    print("Usage: twd <command> [args]")
    print("Commands:")
    print("  upload <file_path> [token]")
    print("  download <file_id> [target]")
    print("  delete <content_id> <token>")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "upload":
        fp = sys.argv[2]
        tok = None
        if len(sys.argv) == 4:
            tok = sys.argv[3]
        upload(fp, tok)
    elif cmd == "download":
        file_id = sys.argv[2]
        target = None
        if len(sys.argv) == 4:
            target = sys.argv[3]
        download(file_id, target)
    elif cmd == "delete":
        content_id = sys.argv[2]
        if len(sys.argv) < 4:
            print("Token required to delete")
            sys.exit(1)
        tok = sys.argv[3]
        delete(content_id, tok)
    else:
        usage()
