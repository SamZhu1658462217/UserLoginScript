import hashlib
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]))
from conf import settings

def getPasswordMd5(string):
    '''
    Encrypt the password entered by the user
    :param string: Password
    :return: md5 string
    '''

    md5 = hashlib.md5()
    md5.update(string.encode('utf-8'))
    return md5.hexdigest()

def checkUserPasswd(username,password,config_obj):
    '''
    Check if the user is a legal user
    :param username: Username
    :param password: Password
    :param config_obj: Account file ConfigParser Object
    :return: Validation results
    '''

    if username in config_obj.sections():
        passwd = config_obj.get(username,'password')
        if password == passwd:
            return True
    return False

def checkUserExists(username,config_obj):

    if username in config_obj.sections():
        return True
    return False

def getUserStatus(username,config_obj):
    '''
    Check if the user is locked
    :param username:  Username
    :param config_obj: Account file ConfigParser Object
    :return: Locked state
    '''

    if config_obj.get(username,'status') == '1':
        return False
    return True

def setUserStatus(username,status,config_obj,configfile):
    '''
    Set the user's lock status
    :param username: Username
    :param status: Lock / Unlock
    :param config_obj: Account file ConfigParser Object
    :param configfile: Account file
    :return: None
    '''

    if status == 'lock':
        accout_status = '1'
    elif status == 'unlock':
        accout_status = '0'
    else:
        raise ValueError('Parser must be lock/unlock')

    with open(configfile,'w') as f:
        config_obj.set(username,'status',accout_status)
        config_obj.write(f)

def writeLog(username,info):
    '''
    log information
    :param username: Username
    :param info: login or lock
    :return:None
    '''

    login_date = time.strftime("%Y-%m-%d", time.localtime())
    login_time = time.strftime("%H:%M:%S", time.localtime())
    login_info = '{} {} Username: {} , Result: {} \n'.format(login_date,login_time,username,info)
    log_file ='{}/login_{}.txt'.format(settings.log_dir,login_date)
    if os.path.exists(log_file):
        status = 'a'
    else:
        status = 'w'
    with open(log_file,status) as f:
        f.write(login_info)




