# encoding: UTF-8
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.db import transaction
from django.core.urlresolvers import reverse
from django.db.models import Q 
from datetime import datetime, timedelta
from bitaopt.util import bita_db
from django.conf import settings
from django.http import HttpResponseRedirect 
import time
import json, urllib
from utestopt.modules.light.report.views import temp
from .api_utils import *
from utestopt.models import BehaveConfig
import sys

# Create your views here.
def user_list_show(request):
    start = request.REQUEST.get('start', '')
    end = request.REQUEST.get('end', '')
    phone_num = request.REQUEST.get('phone_num', '')
    qq_num = request.REQUEST.get('qq_num', '')
    uid = request.REQUEST.get('uid', '')
    level = request.REQUEST.get('level', '')
    status = request.REQUEST.get('status', '')
    type = request.REQUEST.get('type', '')
    
    print 'qq_num = ' + qq_num
    print 'phone_num = ' + phone_num
    
    if not start and ('start' not in request.REQUEST):
        start = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    
    if qq_num:       
        user_list_sql = 'SELECT a.regtime, a.uid, a.nickname, a.LEVEL, a.STATUS, a.TYPE FROM t_user a LEFT JOIN t_user_mapper b ON a.uid = b.uid WHERE '
        if qq_num:
            user_list_sql += 'b.cuid like \'%%' + qq_num + '%%\''
        if level:
            user_list_sql += ' and a.level = \'' + level + '\''
        if status:
            user_list_sql += ' and a.status = \'' + status + '\''
        if type:
            user_list_sql += ' and a.type = \'' + type + '\''
            
        user_list_sql += ' ORDER BY a.regtime DESC'
                    
        print "user_list_sql = " + user_list_sql
            
        user_list_result = bita_db.fetchall(settings.UTEST_USER, user_list_sql)
        user_list_source = [u for u in user_list_result]
          
    elif phone_num:
        user_list_sql = 'SELECT a.regtime, a.uid, a.nickname, a.LEVEL, a.STATUS, a.TYPE FROM t_user a LEFT JOIN t_user_advance b ON a.uid = b.uid WHERE '
        if phone_num:
            user_list_sql += 'b.tel = \'' + phone_num + '\''
        if level:
            user_list_sql += ' and a.level = \'' + level + '\''
        if status:
            user_list_sql += ' and a.status = \'' + status + '\''
        if type:
            user_list_sql += ' and a.type = \'' + type + '\''
            
        user_list_sql += ' ORDER BY a.regtime DESC'
                    
        print "user_list_sql = " + user_list_sql
            
        user_list_result = bita_db.fetchall(settings.UTEST_USER, user_list_sql)
        user_list_source = [u for u in user_list_result]
        
    elif uid:
        user_list_sql = 'SELECT regtime, uid, nickname, level, status, type FROM t_user WHERE '
        if uid:
            user_list_sql += 'uid = \'' + uid + '\''
        if level:
            user_list_sql += ' and level = \'' + level + '\''
        if status:
            user_list_sql += ' and status = \'' + status + '\''
        if type:
            user_list_sql += ' and type = \'' + type + '\''
            
        user_list_sql += ' ORDER BY regtime DESC'
                    
        print "user_list_sql = " + user_list_sql
            
        user_list_result = bita_db.fetchall(settings.UTEST_USER, user_list_sql)
        user_list_source = [u for u in user_list_result]    
    
    else:           
        user_list_sql = 'SELECT regtime, uid, nickname, level, status, type FROM t_user WHERE '
        if start:
            user_list_sql += 'regtime >= \'' + start + '\''
        if end:
            end = end + ' 23:59:59'
            user_list_sql += ' and regtime <= \'' + end + '\''
        if level:
            user_list_sql += ' and level = \'' + level + '\''
        if status:
            user_list_sql += ' and status = \'' + status + '\''
        if type:
            user_list_sql += ' and type = \'' + type + '\''
            
        user_list_sql += ' ORDER BY regtime DESC'
                    
        print "user_list_sql = " + user_list_sql
            
        user_list_result = bita_db.fetchall(settings.UTEST_USER, user_list_sql)
        user_list_source = [u for u in user_list_result]  
    
    user_list = []
    for row in user_list_source:
        temp = []     
        regtime = row[0]
        time_str = datetime.strftime(regtime, '%Y-%m-%d %H:%M:%S')
        temp.append(time_str)
        temp.append(row[1])
        temp.append(row[2])
        temp.append(row[3])
        temp.append(row[4])
        temp.append(row[5])
        user_list.append(temp)
    
    print "user_list = " + str(user_list)
        
    return render(request, 'utest/config/index.html', {
        'user_list': user_list,
        'conditions':{
            'start' : start,
            'end'   : end[0:10],
            'phone_num': phone_num,
            'qq_num': qq_num,
            'uid': uid,
            'level': level,
            'status': status,
            'type': type,
         }
    })
   
    
def user_info_config(request): 
    uid = request.REQUEST.get('uid', '')
    
    if uid:
        user_info = get_user_info(uid)
                      
        return render(request, 'utest/config/edit.html', {
            'time': user_info[0],
            'uid': user_info[1],
            'nickname': user_info[2],
            'level': user_info[3],
            'status': user_info[4],
            'type': user_info[5],      
        })
    else:
        return render(request, 'utest/config/edit.html', {})
  
def save_info(request):
    uid = request.REQUEST.get('uid', '')
    time = request.REQUEST.get('time', '')
    nickname = request.REQUEST.get('nickname', '')
    level = request.REQUEST.get('level', '')
    status = request.REQUEST.get('status', '')
    type = request.REQUEST.get('type', '')
    
    user_info = get_user_info(uid)
      
    if uid != "" and uid != " ":
        save_sql = 'update t_user' + \
        ' set level = \'' + str(level) + \
        '\', status = \'' + str(status) + \
        '\' where uid = \'' + str(uid) + '\''
            
        bita_db.fetchall(settings.UTEST_USER, save_sql)
        
    #判断被改变的字段
    level_pre = str(user_info[3])
    status_pre = str(user_info[4])
    if level_pre != level and status_pre != status:
        str_detail = 'level,status'
        send_notice_to_server(uid, str_detail)  
    elif level_pre != level:
        str_detail = 'level'
        send_notice_to_server(uid, str_detail)  
    elif status_pre != status:
        str_detail = 'status'
        send_notice_to_server(uid, str_detail)  
     
    return HttpResponseRedirect("/utest/config/user_list")

def get_user_info(uid):
    if uid:
        user_info_sql = 'SELECT regtime, uid, nickname, level, status, type FROM t_user WHERE '
        user_info_sql += 'uid = \'' + uid + '\''
                    
        print "user_info_sql = " + user_info_sql
            
        user_info_result = bita_db.fetchall(settings.UTEST_USER, user_info_sql)
        user_info_source = [u for u in user_info_result]
        
        user_info = []
        for row in user_info_source:        
            regtime = row[0]
            time_str = datetime.strftime(regtime, '%Y-%m-%d %H:%M:%S')
            user_info.append(time_str)
            user_info.append(row[1])
            user_info.append(row[2])
            user_info.append(row[3])
            user_info.append(row[4])
            user_info.append(row[5])
        
        print "user_info = " + str(user_info)
    return user_info

def send_notice_to_server(uid, str_detail):
    
    notice_response = send_notice(uid, str_detail)
    notice_json = json.loads(notice_response)
    ret = notice_json['ret']
    if ret == 0:
        print 'send notice success!'
    if ret == 1:
        print 'request param error'
    if ret == 2:
        print 'handling exceptions'
    if ret == 3:
        print 'no method'
        
def data_config_list(request):
    behave_id = request.REQUEST.get('behave_id', '')
    channel_id = request.REQUEST.get('channel_id', '')
    
    cond1 = Q()
    if behave_id:
        cond1 = cond1 & Q(behid=behave_id)
    if channel_id:
        cond1 = cond1 & Q(channel=channel_id)
    
    behave_list = BehaveConfig.objects.values('id', 'behid', 'channel', 'chinesename').filter(cond1).order_by('-id')
    
    return render(request, 'utest/config/behave_list.html', {
        'behave_list': behave_list,
        'conditions':{
            'behave_id': behave_id,
            'channel_id': channel_id,   
         }                                                       
    })
    
def data_config_save(request):
    save_id = request.REQUEST.get('save_id', '')
    save_behid = request.REQUEST.get('save_behid', '')
    save_channel = request.REQUEST.get('save_channel', '')
    save_name = request.REQUEST.get('save_name', '')
    
    reload(sys)
    sys.setdefaultencoding( "utf-8" )  
    print save_name.encode('utf8')

    save_data_config_sql = 'insert into chinese_behave (behid, channel, chinesename) values (\''
    save_data_config_sql += str(save_behid) + '\',\''
    save_data_config_sql += str(save_channel) + '\',\''
    save_data_config_sql += str(save_name) + '\')'
        
    bita_db.fetchall(settings.UTEST_STATISTICS, save_data_config_sql)
    
    return HttpResponseRedirect("/utest/config/data_config")

def data_config_update(request):
    update_id = request.REQUEST.get('update_id', '')
    update_behid = request.REQUEST.get('update_behid', '')
    update_channel = request.REQUEST.get('update_channel', '')
    update_name = request.REQUEST.get('update_name', '')
    
    reload(sys)
    sys.setdefaultencoding( "utf-8" )  
    print update_name.encode('utf8')
    
    if update_id:
        update_id = update_id.strip('【')
        update_id = update_id.strip('】')
        
        print '------------------update_date_sql---------------'
        print update_id
        print '------------------update_date_sql---------------'
        
        update_date_sql = 'update chinese_behave' + \
        ' set behid = \'' + str(update_behid) + \
        '\', channel = \'' + str(update_channel) + \
        '\', chinesename = \'' + str(update_name) + \
        '\' where id = \'' + str(update_id) + '\''
        
        bita_db.fetchall(settings.UTEST_STATISTICS, update_date_sql)
    
    return HttpResponseRedirect("/utest/config/data_config")

def data_config_delete(request):
    data_id = request.REQUEST.get('dataId', '')
    print data_id
    if data_id:
        delete_data_sql = 'delete from chinese_behave where '
        delete_data_sql += 'id = \'' + str(data_id) + '\''
        bita_db.fetchall(settings.UTEST_STATISTICS, delete_data_sql)
    
    return HttpResponseRedirect("/utest/config/data_config")

 #this function is used for config data for http://bitatest.cs0309.imtt.qq.com/
#author RTX  haliluyafu
#date 2016-11
#input 1 : cmd
#imput 2 : parameter1
#impyt 3 : parameter2
def config_test_data(request):
    #db  utest_user_test
    userCMD = request.REQUEST.get('cmd',   'bad_or_empty')
    pra1 = request.REQUEST.get('pra1',   'bad_or_empty')

    print userCMD
    print pra1

    requestData = request.GET

    if len(requestData) == 0:
        print "empty"
        data = {
            "info": 'command empty  .   you can use follow command',
            "function   :   autopay": 'auto finish MIDASHI pay  for your uid at bitatest',
            #"function   :   recharge": 'recharge you U money to 1000'
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        print 'ok.cmd is not empty'

    if userCMD != 'autopay' and userCMD != 'recharge':
        print "bad_cmd"
        data = {
            "info": 'command error  .   you can use follow command',
            "function   :   autopay": 'auto finish MIDASHI pay  for your uid at bitatest',
            "example": 'config_test_data?cmd=autopay&pra1=b8f6f6a3be9a41b3b971c1735bb12c80'
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        print 'ok.cmd is ok'

    if userCMD == 'autopay' and requestData.get('pra1'):
        print userCMD
        uid = requestData.get('pra1')
        print '[' + uid + ']'
        if len(uid) == 0:
            data = {
                "info": 'command error  .   parameter is empty',
                "function   :   autopay": 'auto finish MIDASHI pay  for your uid at bitatest',
                "example": 'config_test_data?cmd=autopay&pra1=b8f6f6a3be9a41b3b971c1735bb12c80'
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            print 'ok pra1 is not empty'

            #safety process
            uid = uid.replace('<','')
            uid = uid.replace('>', '')
            uid = uid.replace("'", "")

            mysql = ("SELECT pay_order_info.id,pay_order_info.utest_money,pay_order_info.`status` FROM pay_order_info WHERE pay_order_info.uid LIKE '"
                    + uid
                    + "' ORDER BY pay_order_info.submit_time DESC LIMIT 0, 1")
            print mysql
            myresult = bita_db.fetchall("utest_user_test_pay", mysql)
            if len(myresult) == 0:
                print "uid is not right"
                data = {
                    "info": 'uid is not right',
                    "function   :   autopay": 'auto finish MIDASHI pay  for your uid at bitatest',
                    "example": 'config_test_data?cmd=autopay&pra1=b8f6f6a3be9a41b3b971c1735bb12c80'
                }
                return HttpResponse(json.dumps(data), content_type="application/json")
            payid = str(myresult[0][0])
            paymoney = str(int(myresult[0][1]))
            paystate = str(myresult[0][2])
            print payid
            print paymoney
            print paystate
            if paystate != 'success':
                midashiHttp = ("http://10.229.135.152:8080/paymentserver/pay/payCallBack?amt="
                +paymoney
                +"00&appid=1450005683&billno=-UCHLZY-20160827-1627382413&cftid=10000189%2001321608272960639630&openid="
                +payid
                +"&payamt_coins=0&paychannel=wechat&paychannelsubid=1&payitem=U1*1*10&pbazinga=1&providetype=0&pubacct_payamt_coins&token=9DEEB50D4373A396E6D9CC598761B19B20308&ts=1472286702&version=v3&zoneid=0&sig=n63XfoEK6zfUnGdj2qeCDW5jssE%3D")
                print midashiHttp
                tempreq = urllib2.Request(midashiHttp)
                print tempreq
                temprsp = urllib2.urlopen(tempreq)
                tempinfo = temprsp.read()
                print tempinfo
                data = {
                    "info": 'last id = ' + payid + ' is success payed ^-^',
                    "function   :   autopay": 'auto finish MIDASHI pay  for your uid at bitatest',
                    "example": 'config_test_data?cmd=autopay&pra1=b8f6f6a3be9a41b3b971c1735bb12c80'
                }
                return HttpResponse(json.dumps(data), content_type="application/json")

            else:
                print 'last id = ' + payid + ' is already payed '
                data = {
                    "info": 'last id = ' + payid + ' is already payed -_-',
                    "function   :   autopay": 'auto finish MIDASHI pay  for your uid at bitatest',
                    "example": 'config_test_data?cmd=autopay&pra1=b8f6f6a3be9a41b3b971c1735bb12c80'
                }
                return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        data = {
            "info": 'pra1 is need',
            "function   :   autopay": 'auto finish MIDASHI pay  for your uid at bitatest',
            "example": 'config_test_data?cmd=autopay&pra1=b8f6f6a3be9a41b3b971c1735bb12c80'
        }
        return HttpResponse(json.dumps(data), content_type="application/json")


    print 'end of function config_test_data'
    data = {
        "info": 'end of function config_test_data',
    }
    return HttpResponse(json.dumps(data), content_type="application/json")

def get_time_str(later = 0):
    nowtime = time.time()
    nowtime += later*60
    current_time = time.localtime(nowtime)
    return time.strftime('%Y-%m-%d %H:%M:%S', current_time)

def generate_testdata_01(request):
    print "generate_testdata_01"

    uid = '12345678'
    h5_pressure_task_uid = '12345678'
    h5_pressure_task_task_name = '白盒自动化数据'
    h5_pressure_task_submit_url = 'http://halei.win:3000/'
    h5_pressure_task_web_title = '这个标题开起来长11111111111111111111112222222222222222222223333333333333333333333333'
    h5_pressure_task_image_url = 'http://sznk.fcloud.store.qq.com/store_raw_download?buid=17201&uuid=10001_196ff954f8ac5d5c01975c6a4e768428111-1111-3_20161117164615@node8.png'
    h5_pressure_task_virtual_user_num = '20'
    h5_pressure_task_round_num = '5'
    h5_pressure_task_finish_rounds = '5'
    h5_pressure_task_space_time = '60'
    h5_pressure_task_submit_time = get_time_str()
    h5_pressure_task_finish_time = get_time_str(6)
    h5_pressure_task_last_status_time = get_time_str(6)
    h5_pressure_task_status = 'finish'
    h5_pressure_task_score = '98'

    # --------1-----------task
    sqltemp_insert_t_h5_pressure_task = "INSERT INTO t_h5_pressure_task(uid, task_name, submit_url,web_title,image_url,virtual_user_num,round_num,finish_rounds,space_time,submit_time,finish_time,last_status_time,status,score)  VALUES( " \
                                    "'%s','%s','%s','%s','%s',%s,%s,%s,%s,'%s','%s','%s','%s',%s);"
    sql_insert_t_h5_pressure_task = sqltemp_insert_t_h5_pressure_task%(h5_pressure_task_uid,h5_pressure_task_task_name,h5_pressure_task_submit_url,h5_pressure_task_web_title,h5_pressure_task_image_url,
                                                                       h5_pressure_task_virtual_user_num,h5_pressure_task_round_num,h5_pressure_task_finish_rounds,h5_pressure_task_space_time,
                                                                       h5_pressure_task_submit_time,h5_pressure_task_finish_time,h5_pressure_task_last_status_time,h5_pressure_task_status,h5_pressure_task_score)



    print sql_insert_t_h5_pressure_task
    myresult = bita_db.fetchall("utest_user_test_pressure", sql_insert_t_h5_pressure_task)
    print myresult

    mysql =  "SELECT t_h5_pressure_task.task_id FROM t_h5_pressure_task ORDER BY t_h5_pressure_task.task_id DESC LIMIT 0, 1 ;"
    print mysql
    myresult = bita_db.fetchall("utest_user_test_pressure", mysql)
    last_id = myresult[0][0]
    print last_id





    print "generate_testdata_02"

    data = {
        "info": 'ok',
        "test_sql":sql_insert_t_h5_pressure_task,
        "last_id":last_id
    }
    return HttpResponse(json.dumps(data), content_type="application/json")
