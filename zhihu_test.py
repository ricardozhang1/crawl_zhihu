#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import os
import requests



#模拟知乎登陆
def get_loggin_cookie():
    '''获取知乎的cookie值,并保存到本地'''
    driver = webdriver.Chrome()
    url = 'https://www.zhihu.com/signup?next=%2F#signin'
    driver.get(url)
    time.sleep(3)
    driver.find_element_by_css_selector('.SignContainer-switch span').click()
    driver.find_element_by_css_selector('.SignFlow-accountInput.Input-wrapper input').send_keys('13559230717')
    driver.find_element_by_css_selector('.SignFlow-password .SignFlowInput .Input-wrapper input').send_keys('zcw112')
    time.sleep(10)
    driver.find_element_by_css_selector('.Button.SignFlow-submitButton.Button--primary.Button--blue').click()
    time.sleep(3)
    cookie = [ item["name"] + "=" + item["value"] for item in driver.get_cookies()]
    cookiestr = ';'.join(item for item in cookie)
    with open('cookies.txt','w') as f:
        f.write(cookiestr)
        f.close()


def get_loggin():
    '''根据已存cookie进行登录知乎首页'''
    path_object = os.path.abspath(os.path.dirname(__file__))
    with open('{0}\cookies.txt'.format(path_object),'r') as f:
        cookie =f.read()
    cookies = {}
    for line in cookie.split(';'):
        name,value = line.strip().split('=',1)
        cookies[name] = value.replace('"','')
    return cookies




