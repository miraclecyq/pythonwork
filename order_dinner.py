#!/usr/bin/env python
# -*- coding=utf-8 -*-

# order_dinner.py

import urllib
import urllib2
import json
import sys
import time
import requests

LOGIN_API = 'http://wcent.duitang.net/napi/login/checkpwd/'

ORDER_API = 'http://wcent.duitang.net/napi/backend/dinner/book/'

NOTICE_API = 'http://wcent.duitang.net/napi/message/warn/'

ORDER_LIST_API = 'http://wcent.duitang.net/napi/backend/dinner/list/'

ORDER_MENU_API = 'http://wcent.duitang.net/napi/backend/dinner/menu/'

PEOPLE_LIST_MAP = {'0086':'左左', '0098': '大哼', '0067': '海波', '0100': '雪糕', '1040': '小K',}

PEOPLE_ID_LIST = [u_id for u_id in PEOPLE_LIST_MAP.keys()]

# 使得 sys.getdefaultencoding() 的值为 'utf-8'  
reload(sys)                      # reload 才能调用 setdefaultencoding 方法  
sys.setdefaultencoding('utf-8')  # 设置 'utf-8'  

login_data = {
    'loginname': '0086',
    'password': 'asd123456.',
}

def get_common_opener():
    params = urllib.urlencode(login_data)
    req = urllib2.Request(LOGIN_API, params)
    cookies = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(cookies)
    urllib2.install_opener(opener)
    response = opener.open(req)
    # response = urllib2.urlopen(req)
    the_page = response.read()
    print '登陆成功!' if json.loads(the_page).get('status') == 1 else '登陆失败'
    return opener

def get_session():
    """
    requests的session对象,可以保存当前session状态，包括cookie
    """
    s = requests.session()
    s.post(url=LOGIN_API, data=login_data)
    return s

def run():
    order_result = False
    
    # ---------------
    opener = get_common_opener()
    s = get_session()
    # ---------------


    order_dinner_list_result = opener.open(ORDER_LIST_API)
    try:
        memo_result = get_memo(order_dinner_list_result.read())
    except Exception, e:
        print e
        memo_result = {'success': False}

    order_info = {
        'count':'1',
        'memo':'',
        'platform':'WEB',
    }
    if not memo_result.get('success') or len(memo_result.get('memo_ids')) < 1:
        # order_result = order_dinner(get_common_opener(), order_info)
        params = urllib.urlencode(order_info)
        req = urllib2.Request(ORDER_API, params)
        response = opener.open(req)
    else:
        people_info_list = [PEOPLE_LIST_MAP.get(memo_id) for memo_id in memo_result.get('memo_ids')]
        success_people_num = 0
        for people_info in people_info_list:
            order_info['memo'] = '%s +1' % people_info
            # if order_dinner(get_common_opener(), order_info):
            #     time.sleep(1)
            params = urllib.urlencode(order_info)
            req = urllib2.Request(url=ORDER_API, data=params)
            # r = requests.post(ORDER_API, data=order_info)
            # print r.json()
            # response = opener.open(req)
            r = s.post(url=ORDER_API, data=order_info)
            # print(r, order_info)
            success_people_num += 1
            time.sleep(11) # 订餐后台不允许10秒内重复操作
        if (success_people_num != len(people_info_list)):
            return False

    notice_target = '0086,%s' % ','.join([memo_id for memo_id in memo_result.get('memo_ids')])
    today_menu = get_today_menu(s)
    message = '订餐成功!今日晚餐- %s' % today_menu
    send_notice(notice_target, message)

    message = '到订餐时间了,小伙子,今天是 %s' % today_menu
    send_need_order_message(message)
    return True

def get_today_menu(session):
    r = session.get(ORDER_MENU_API)
    data = json.loads(r.text).get('data')
    dayOfWeek = str(data.get('dayOfWeek'))
    menu = data.get('menu')
    return menu.get(dayOfWeek)

def send_notice(target, message):
    data = {
        'receivers': target,
        'desc': message,
        'clients': 'wechat',
    }
    param = urllib.urlencode(data)
    urllib2.urlopen(url=NOTICE_API, data=param)

def send_need_order_message(message):
    notice_target = '0077'
    send_notice(notice_target, message)

def order_dinner(opener, order_info):
    """
    使用urllib2.OpenerDierctor操作
    """
    params = urllib.urlencode(order_info)
    req = None
    response = None
    try:
        req = urllib2.Request(ORDER_API, params)
        response = opener.open(req)
        pass
    except Exception, e:
        print e
        return False
    return True

def get_memo(order_dinner_list):
    # 添加替订boy
    # 1. 检查该boy是否已自己点餐
    order_dinner_list_json = json.loads(order_dinner_list)
    status = order_dinner_list_json.get('status')
    memo_ids = []
    if not status or status != 1:
        return {'success': False}
    logs = order_dinner_list_json.get('data').get('logs')
    order_id_list = [str(log['contact']['userId']) for log in logs]

    for need_order_id in PEOPLE_ID_LIST:
        if need_order_id =='0086':
            memo_ids.append(need_order_id) # 过滤点餐账号
            continue
        if need_order_id in order_id_list:
            print need_order_id, '%s 娃已点' % PEOPLE_LIST_MAP.get(need_order_id)
            continue
        user_name = PEOPLE_LIST_MAP.get(need_order_id, None)
        if not user_name:  
            continue
        memo_ids.append(need_order_id) # 2.未点，加入代点id名单
    return {'success': True, 'memo_ids': memo_ids}


if __name__ == '__main__':
    # get_common_opener()
    if run():
        print '点餐任务完成'
        pass
    else:
        notice_target = '0086'
        message = '点餐出现问题，请手动点餐.'
        send_notice(notice_target, message)
