#!/bin/bash
API_UPLOAD="https://upload.gofile.io/uploadFile"
API_CONTENT="https://api.gofile.io/getContent"

cmd=$1
if [ "$cmd" == "upload" ]; then
  file=$2
  if [ ! -f "$file" ]; then echo "File not exists"; exit 1; fi
  response=$(curl -s -F "file=@$file" $API_UPLOAD)
  fileId=$(echo $response | jq -r '.data.fileId')
  dl=$(echo $response | jq -r '.data.downloadPage')
  echo "File ID: $fileId"; echo "Download page: $dl"
elif [ "$cmd" == "download" ]; then
  fileId=$2
  target=$3
  link=$(curl -s "$API_CONTENT?contentId=$fileId" | jq -r '.data.directLinkList[0]')
  if [ -z "$target" ]; then target=$(basename $link); fi
  curl -L "$link" -o "$target"
  echo "Downloaded to: $target"
else
  echo "Usage: ./twd.sh <upload|download> <file|file_id> [target]"
fi
