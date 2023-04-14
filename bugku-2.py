import requests
import ddddocr
import binascii
r=requests.session()
ocr=ddddocr.DdddOcr()
url="https://ctf.bugku.com/login"
url2="https://ctf.bugku.com/captcha.html"
def save_img():
    req=r.get(url)
    cap=r.get(url2).content
    cap=binascii.b2a_hex(cap)
    with open("C:\\Users\\D1oMg\\Desktop\\1.png","wb") as f:
        bin=binascii.unhexlify(cap)
        f.write(bin)
        f.close()

def code():
    global res
    with open("C:\\Users\\D1oMg\\Desktop\\1.png","rb") as k:
        read=k.read()
    res=ocr.classification(read)
    # print(res)

def login(res):
    print()

if __name__=="__main__":
    save_img()
    code()
    login()