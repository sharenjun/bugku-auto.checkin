import requests
import ddddocr
import binascii
import re
r=requests.session()
ocr=ddddocr.DdddOcr()
url="https://ctf.bugku.com/login"
url2="https://ctf.bugku.com/captcha.html0.7240433493056317"
url3="https://ctf.bugku.com//login/check.html"
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
class all():
    def captcha(self):
        cap=r.get(url2).content
        cap=binascii.b2a_hex(cap)
        with open("C:\\Users\\D1oMg\\Desktop\\1.png","wb") as f:
            bin=binascii.unhexlify(cap)
            f.write(bin)
            f.close()
        #读取文件输出验证码
        with open("C:\\Users\\D1oMg\\Desktop\\1.png","rb") as k:
            read=k.read()
        res=ocr.classification(read)
        print(res)
        data={"username":"账号",
        "password":"密码",
        "vcode":"%s"%res,
        "autologin":"1"
        }
        login=r.post(url=url3,data=data,headers=headers)
        text=login.text
        code=text.split(",")[0].split(":")[1]
        success=text.split(",")[1].split(":")[1]
        # print(success)
        # print(code)
        if(text==0):
            self.captcha()
        else:
            check=r.get("https://ctf.bugku.com/user/checkin")
            # print(check.headers)
            # print(check.text)
            ct=check.text
            pipei=re.findall(r'[\u4e00-\u9fa5]+',ct)
            if(pipei[1]=='今天您已经签到过啦'):
                exit
                print("退出成功")
            else:
                self.captcha()
            print(pipei)

        
if __name__=="__main__":
   _a=all()
   _a.captcha()