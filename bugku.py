#一代
import requests

csrftoken="7be910763a8ae3bd45cbad5c806ac13e"
auto="wYsM64dA3ns2hQQsxG98rnS9Z0dSe7yDRqmPRg2MjN4RCuAQkGMdGTGaWMD8%2B3gxsUW9viz5b66VysRePbqKjOxkTAZOTy%2F4UQ1PCKsolE8EZCJ8rNMb1BfiNg2WsgXqUgludbEVzG2n"
sessid="d6c6e0f46db24ccfb0f4ced2f873b9b2"
def check(csrftoken,auto,sessid):
    session = requests.session()
    burp0_url = "https://ctf.bugku.com:443/user/checkin"
    burp0_cookies = {"Hm_lvt_97426e6b69219bfb34f8a3a1058dc596": "1665536491", 
                     "PHPSESSID": sessid, 
                     "autoLogin": auto, 
                     "X-CSRF-TOKEN": csrftoken
                     }
    burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Google Chrome\";v=\"110\"", 
                     "Accept": "*/*", "X-Csrf-Token": csrftoken, 
                     "X-Requested-With": "XMLHttpRequest", 
                     "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36", 
                     "Sec-Ch-Ua-Platform": "\"Windows\"", 
                     "Sec-Fetch-Site": "same-origin", 
                     "Sec-Fetch-Mode": "cors", 
                     "Sec-Fetch-Dest": "empty", 
                     "Referer": "https://ctf.bugku.com/index.html", 
                     "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9"}
    a=session.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)
    print(a.text)

check(csrftoken,auto,sessid)

#二代


