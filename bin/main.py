import os
import sys
sys.path.append(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]))

from libs import tools
from conf import settings
import time
import configparser

def menu(username):
    '''
    Welcome page
    :param username: user input username
    :return: None
    '''

    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print('''
    User: {}
    info: Welcome Login !
    time: {}
    '''.format(username,now))

def loginPage():
    '''
    login menu,Collect user input information
    :return:Username and Password
    '''

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

    # 记录用户重试次数
    user_status_dic = {}

    # 主逻辑
    while True:
        username,password = loginPage()
        if tools.checkUserExists(username,cp):      # 检查是否是合法用户
            if tools.getUserStatus(username,cp):    # 检查用户是否被锁定
                if username not in user_status_dic: # 检查用户是否是第一次登陆
                    user_status_dic[username] = 1   # 初始化当前用户重试次数
            else:
                print('\033[31mThe Account: [ {} ] is locking!,retry other account\033[0m'.format(username))
                continue
        else:
            print('\033[31mUser: [ {} ] is not exists!\033[0m'.format(username))
            continue
        password = tools.getPasswordMd5(password)
        if tools.checkUserPasswd(username,password,cp):
            menu(username)
            tools.writeLog(username,'login')
            break
        else:
            if user_status_dic[username] == settings.login_retry:   # 用户尝试次数到达阈值
                print('\033[31mSorry，The Accout: [ {} ] will be locking!\033[0m'.format(username))
                tools.setUserStatus(username,'lock',cp,settings.accout_file)  # 锁定用户
                tools.writeLog(username, 'lock')
                break
            print('\033[31mPassword is Wrong,please retry\033[0m')
            tools.writeLog(username, 'Wrong Password')
            user_status_dic[username] += 1   # 错误重试次数自加