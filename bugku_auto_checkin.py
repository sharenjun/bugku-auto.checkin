import os
import sys
import time
import json
import base64
from datetime import datetime
import requests
from PIL import Image
from io import BytesIO
import ddddocr


class BugkuAutoCheckin:
    def __init__(self, username=None, password=None):
        """
        初始化签到器
        
        Args:
            username (str): 用户名
            password (str): 密码
        """
        self.username = username or os.getenv('BUGKU_USERNAME')
        self.password = password or os.getenv('BUGKU_PASSWORD')
        
        # 检查是否提供了凭据
        if not self.username or not self.password:
            raise ValueError("请提供用户名和密码（通过参数或环境变量 BUGKU_USERNAME/BUGKU_PASSWORD）")
        
        # 创建会话对象以保持登录状态
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # 初始化OCR
        self.ocr = ddddocr.DdddOcr()
        
        # 定义URL常量
        self.login_url = 'https://ctf.bugku.com/login/check.html'
        self.checkin_url = 'https://ctf.bugku.com/user/sign.html'
        self.captcha_url = 'https://ctf.bugku.com/common/captcha.html'
        self.login_page_url = 'https://ctf.bugku.com/login.html'

    def get_captcha(self):
        """
        获取验证码图片并识别
        
        Returns:
            str: 识别出的验证码文本
        """
        try:
            response = self.session.get(self.captcha_url, timeout=10)
            response.raise_for_status()
            
            # 识别验证码
            captcha_text = self.ocr.classification(response.content)
            print(f"[DEBUG] 验证码识别结果: {captcha_text}")
            return captcha_text
            
        except requests.RequestException as e:
            print(f"[ERROR] 获取验证码失败: {e}")
            return None
        except Exception as e:
            print(f"[ERROR] 验证码识别失败: {e}")
            return None

    def login(self):
        """
        执行登录操作
        
        Returns:
            bool: 登录成功返回True，否则返回False
        """
        max_retries = 3
        
        for attempt in range(max_retries):
            print(f"[INFO] 尝试登录... (第{attempt + 1}次)")
            
            # 获取验证码
            captcha = self.get_captcha()
            if not captcha:
                print("[ERROR] 验证码获取失败，跳过本次登录尝试")
                continue
            
            # 构建登录数据
            login_data = {
                'username': self.username,
                'password': self.password,
                'code': captcha,
                'remenber': '1'
            }
            
            try:
                # 发送登录请求
                response = self.session.post(
                    self.login_url,
                    data=login_data,
                    timeout=15
                )
                
                # 解析响应
                try:
                    result = response.json()
                    print(f"[DEBUG] 登录响应: {result}")
                    
                    if result.get('status') == 1:
                        print("[SUCCESS] 登录成功！")
                        return True
                    else:
                        error_msg = result.get('msg', '未知错误')
                        print(f"[ERROR] 登录失败: {error_msg}")
                        
                        # 如果是验证码错误，继续下一次尝试
                        if '验证码' in error_msg or 'code' in error_msg.lower():
                            print("[INFO] 验证码可能有误，准备重试...")
                            time.sleep(1)
                            continue
                        else:
                            # 其他错误直接返回
                            return False
                            
                except json.JSONDecodeError:
                    print(f"[ERROR] 响应不是有效的JSON格式: {response.text[:200]}...")
                    return False
                    
            except requests.RequestException as e:
                print(f"[ERROR] 登录请求失败: {e}")
                if attempt < max_retries - 1:
                    print("[INFO] 准备重试...")
                    time.sleep(2)
                continue
        
        print("[ERROR] 达到最大重试次数，登录失败")
        return False

    def checkin(self):
        """
        执行签到操作
        
        Returns:
            bool: 签到成功返回True，否则返回False
        """
        try:
            print("[INFO] 开始执行签到...")
            
            # 发送签到请求
            response = self.session.post(
                self.checkin_url,
                timeout=15
            )
            
            # 解析响应
            try:
                result = response.json()
                print(f"[DEBUG] 签到响应: {result}")
                
                if result.get('status') == 1:
                    print(f"[SUCCESS] 签到成功！获得积分: {result.get('data', {}).get('score', '未知')}")
                    return True
                else:
                    error_msg = result.get('msg', '未知错误')
                    print(f"[ERROR] 签到失败: {error_msg}")
                    return False
                    
            except json.JSONDecodeError:
                print(f"[ERROR] 签到响应不是有效的JSON格式: {response.text[:200]}...")
                return False
                
        except requests.RequestException as e:
            print(f"[ERROR] 签到请求失败: {e}")
            return False

    def run(self):
        """
        执行完整的签到流程
        """
        print(f"[INFO] 开始执行签到任务 - 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 尝试登录
        if not self.login():
            print("[FATAL] 登录失败，无法继续执行签到")
            return False
        
        # 登录成功后执行签到
        success = self.checkin()
        
        print(f"[INFO] 签到任务完成 - 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return success


def main():
    """主函数"""
    # 从命令行参数或环境变量获取凭据
    username = None
    password = None
    
    # 尝试从命令行参数获取
    if len(sys.argv) >= 3:
        username = sys.argv[1]
        password = sys.argv[2]
    
    try:
        # 创建签到器实例
        checkiner = BugkuAutoCheckin(username, password)
        
        # 执行签到
        success = checkiner.run()
        
        # 根据结果设置退出码
        sys.exit(0 if success else 1)
        
    except ValueError as e:
        print(f"[ERROR] {e}")
        print("\n使用方法:")
        print("1. 设置环境变量: export BUGKU_USERNAME=your_username && export BUGKU_PASSWORD=your_password")
        print("2. 直接传入参数: python bugku_auto_checkin.py <username> <password>")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[INFO] 用户中断程序")
        sys.exit(130)
    except Exception as e:
        print(f"[ERROR] 程序执行出错: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()