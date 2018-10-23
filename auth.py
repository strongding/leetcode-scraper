import os
import requests
import http.cookiejar


USERNAME='username'
PASSWORD='password'
BASE_URL = 'https://leetcode.com'
LOGIN_URL = BASE_URL + '/accounts/login/'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
    'Connection': 'keep-alive',
    'Host': 'leetcode.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
    'Referer': 'https://leetcode.com/accounts/login/',
}

HOME = os.path.expanduser('~')
CONFIG_FOLDER = os.path.join(HOME, '.config', 'leetcode')
COOKIE_PATH = os.path.join(CONFIG_FOLDER, 'cookies')

session=requests.session()
session.cookies=http.cookiejar.LWPCookieJar(COOKIE_PATH)
try:
    session.cookies.load(ignore_discard=True)
except:
    pass


def retrieve(url, headers=None, method='GET', data=None):
    try:
        if method == 'GET':
            r = session.get(url, headers=headers)
        elif method == 'POST':
            r = session.post(url, headers=headers, data=data)
        return r
    except requests.exceptions.RequestException as e:
        print(e)
        pass

def login_in():
    login_data={}
    r=retrieve(LOGIN_URL, headers)
    if r.status_code != 200:
        print('login fails')
        return False
    if 'csrftoken' in r.cookies:
        csrftoken = r.cookies['csrftoken']
        login_data['csrfmiddlewaretoken'] = csrftoken
    login_data['login'] = USERNAME
    login_data['password'] = PASSWORD
    login_data['remember'] = 'on'
    r=retrieve(LOGIN_URL, headers=headers, method='POST', data=login_data)
    if r.status_code != 200:
        print('login fails')
        return False
    print('login success')
    session.cookies.save()
    return True