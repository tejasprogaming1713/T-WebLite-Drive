#!/usr/bin/env python3

import sys
import os
from anonfile import AnonFile  # using the anonfile Python API wrapper 0

def list_files():
    """
    Note: Anonfiles API doesn't provide a way to list all files anonymously.
    This function will just print a message.
    """
    print("⚠️ Listing is not supported with Anonfiles anonymous API.")

def upload(file_path):
    """Upload a file to AnonFiles."""
    if not os.path.exists(file_path):
        print("Error: File does not exist:", file_path)
        return

    anon = AnonFile()
    result = anon.upload(file_path, progressbar=True)
    url = result.url.geturl()
    print("Uploaded successfully! URL:", url)

def download(link, target=None):
    """Download a file from AnonFiles link."""
    anon = AnonFile()
    # If target directory is given, download there else current directory
    out = anon.download(link, path=target)  # default path = cwd 1
    print("Downloaded to:", out.file_path)

def delete(link):
    """
    AnonFiles anonymous API does NOT support deletion via API.  
    This function will just print a message.
    """
    print("⚠️ Delete is not supported via AnonFiles anonymous API.")

def share(file_path):
    """
    For AnonFiles, share link is the same as upload's returned URL.
    So just call upload.
    """
    upload(file_path)

def usage():
    print("Usage: twd <command> [args]")
    print("Commands:")
    print("  list")
    print("  upload <file_path>")
    print("  download <url> [target_folder]")
    print("  share <file_path>")
    print("  delete <url>")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "list":
        list_files()
    elif cmd == "upload":
        if len(sys.argv) < 3:
            print("Error: Provide a file to upload.")
            usage()
        else:
            upload(sys.argv[2])
    elif cmd == "download":
        if len(sys.argv) < 3:
            print("Error: Provide the URL to download.")
            usage()
        else:
            target = None
            if len(sys.argv) == 4:
                target = sys.argv[3]
            download(sys.argv[2], target)
    elif cmd == "share":
        if len(sys.argv) < 3:
            print("Error: Provide the file to share.")
            usage()
        else:
            share(sys.argv[2])
    elif cmd == "delete":
        if len(sys.argv) < 3:
            print("Error: Provide the URL to delete.")
            usage()
        else:
            delete(sys.argv[2])
    else:
        print("Unknown command:", cmd)
        usage()
