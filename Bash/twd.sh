#!/bin/bash

API_UPLOAD="https://upload.gofile.io/uploadFile"
API_CONTENT="https://api.gofile.io/getContent"

cmd=$1

if [ "$cmd" == "upload" ]; then
  file=$2
  token=$3
  if [ ! -f "$file" ]; then
    echo "File does not exist: $file"
    exit 1
  fi

  if [ -z "$token" ]; then
    response=$(curl -s -F "file=@$file" "$API_UPLOAD")
  else
    response=$(curl -s -F "file=@$file" -F "token=$token" "$API_UPLOAD")
  fi

  echo "Response: $response"
  # parse JSON to get fileId and downloadPage using jq
  fileId=$(echo "$response" | jq -r '.data.fileId')
  dl=$(echo "$response" | jq -r '.data.downloadPage')
  echo "File ID: $fileId"
  echo "Download Page: $dl"

elif [ "$cmd" == "download" ]; then
  fileId=$2
  target=$3
  if [ -z "$target" ]; then
    # get link
    json=$(curl -s "$API_CONTENT?contentId=$fileId")
    link=$(echo "$json" | jq -r '.data.directLinkList[0]')
    target=$(basename "$link")
  else
    link=$(curl -s "$API_CONTENT?contentId=$fileId" | jq -r '.data.directLinkList[0]')
  fi
  curl -L "$link" -o "$target"
  echo "Downloaded to: $target"

else
  echo "Usage: twd <upload|download> <args>"
  echo "upload <file_path> [token]"
  echo "download <file_id> [target]"
  exit 1
fi
