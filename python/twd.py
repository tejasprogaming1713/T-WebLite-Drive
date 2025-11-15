#!/usr/bin/env python3
import sys, os, requests

API_UPLOAD = "https://upload.gofile.io/uploadFile"
API_CONTENT = "https://api.gofile.io/getContent"

def upload(file_path):
    if not os.path.exists(file_path):
        print("File does not exist:", file_path)
        return
    files = {'file': open(file_path, 'rb')}
    resp = requests.post(API_UPLOAD, files=files)
    result = resp.json()
    if result['status']:
        print("Uploaded! File ID:", result['data']['fileId'])
        print("Download page:", result['data']['downloadPage'])
    else:
        print("Upload failed:", result)

def download(file_id, target=None):
    resp = requests.get(f"{API_CONTENT}?contentId={file_id}")
    result = resp.json()
    if not result['status']:
        print("Error:", result)
        return
    link = result['data']['directLinkList'][0]
    if not target:
        target = link.split('/')[-1]
    dl = requests.get(link, stream=True)
    with open(target, 'wb') as f:
        for chunk in dl.iter_content(8192):
            f.write(chunk)
    print("Downloaded to:", target)

if __name__=="__main__":
    if len(sys.argv)<3:
        print("Usage: python twd.py <upload|download> <file|file_id> [target]")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd=="upload":
        upload(sys.argv[2])
    elif cmd=="download":
        target = None
        if len(sys.argv)==4:
            target=sys.argv[3]
        download(sys.argv[2], target)
