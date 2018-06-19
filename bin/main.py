import os
import sys
sys.path.append(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]))

from libs import tools
from conf import settings
import time
import configparser

def menu(username):
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print('''
    User: {}
    info: Welcome Login !
    time: {}
    '''.format(username,now))

def loginPage():
    while True:
        print('--------> Login Page <---------')
        username = input('Username: ').strip()
        if not username:
            print('\033[31mError,You must input Username !\033[0m')
            time.sleep(1)
            continue
        password = input('Password: ').strip()
        if not password:
            print('\033[31mPassword not None !\033[0m')
            time.sleep(1)
            continue
        break
    return username,password

if __name__ == '__main__':

    # 读取配置文件
    cp = configparser.ConfigParser()
    cp.read(settings.accout_file,encoding='utf-8')

    n = 0 # 循环次数
    user_status_dic = {} # 记录用户重试次数
    while n < settings.login_retry:
        username,password = loginPage()
        if tools.checkUserExists(username,cp):
            user_status_dic[username] = 3
        password = tools.getPasswordMd5(password)
        if tools.checkUserPasswd(username,password,cp):
            menu(username)
        else:
            print('User')