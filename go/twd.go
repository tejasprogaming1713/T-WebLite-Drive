package main
import (
 "bytes"
 "encoding/json"
 "fmt"
 "io"
 "mime/multipart"
 "net/http"
 "os"
 "path/filepath"
)
const (
 API_UPLOAD  = "https://upload.gofile.io/uploadFile"
 API_CONTENT = "https://api.gofile.io/getContent"
)
type UploadResp struct {
 Status bool `json:"status"`
 Data struct {
  FileId string `json:"fileId"`
  DownloadPage string `json:"downloadPage"`
 } `json:"data"`
}
type ContentResp struct {
 Status bool `json:"status"`
 Data struct { DirectLinkList []string `json:"directLinkList"` } `json:"data"`
}
func upload(filePath string){
 file, _:=os.Open(filePath); defer file.Close()
 body:=&bytes.Buffer{}; writer:=multipart.NewWriter(body)
 part,_:=writer.CreateFormFile("file",filepath.Base(filePath))
 io.Copy(part,file); writer.Close()
 resp,_:=http.Post(API_UPLOAD, writer.FormDataContentType(), body)
 defer resp.Body.Close()
 var r UploadResp; json.NewDecoder(resp.Body).Decode(&r)
 if r.Status{fmt.Println("Uploaded! File ID:", r.Data.FileId, "Download page:", r.Data.DownloadPage)}
 else{fmt.Println("Upload failed")}
}
func download(fileId,target string){
 resp,_:=http.Get(fmt.Sprintf("%s?contentId=%s",API_CONTENT,fileId)); defer resp.Body.Close()
 var r ContentResp; json.NewDecoder(resp.Body).Decode(&r)
 link:=r.Data.DirectLinkList[0]
 out,_:=os.Create(target); defer out.Close()
 dl,_:=http.Get(link); defer dl.Body.Close()
 io.Copy(out,dl.Body)
 fmt.Println("Downloaded to:", target)
}
func main(){
 if len(os.Args)<3{fmt.Println("Usage: twd <upload|download> <file|file_id> [target]"); return}
 cmd, arg1 := os.Args[1], os.Args[2]
 if cmd=="upload"{upload(arg1)}
 if cmd=="download"{target:=""; if len(os.Args)==4{target=os.Args[3]}else{target=arg1+".download"}; download(arg1,target)}
}
