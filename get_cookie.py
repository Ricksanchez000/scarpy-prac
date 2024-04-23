from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
 
 
browser_options = Options()
browser = webdriver.Chrome(options=browser_options)
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                         '/103.0.0.0 Safari/537.36'}
print("浏览器已成功创建。")
 
 
def get_cookie(url='https://passport.weibo.cn/signin/login?'):
    url = url
    browser.get(url)
    print('现在请在Chrome浏览器中登录你的账号。')
    waiting = True
    while waiting:
        ok = input('登录成功后，输入任意内容并按回车键继续。')
        if ok:
            waiting = False
    with open('cookies.txt', 'w') as f:
        f.write(json.dumps(browser.get_cookies()))
        f.close()
    print('已成功保存cookie信息。')
 
 
if __name__ == '__main__':
    get_cookie()