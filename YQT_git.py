import time
import os
import urllib.request
from urllib.parse import quote
import pymysql
import random
#你需要配置下列项目
ipAdress = ''#你的数据库地址
DBUser = 'root'#数据库的名字
DBPassword = ''
DataBase = 'db1'#数据库名
#你自己的SCKEY http://sc.ftqq.com/3.version
myPushId = 'SCU103759T8dd53cfc1e46f6d980727c976e4ae4c05efc8b5783bb5'
#配置结束
morningStartTime = '06:40'
morningEndTime = '09:30'
noneStartTime = '11:40'
noneEndTime='14:30'
nightStartTime = '20:40'
nightEndTime = '22:30'
morningK = 0 #0:没有
noneK = 0
nightK = 0
YiQingTongK = 0
YQTStartTime = '13:10'
YQTEndTime = '16:00'
YQTSecondTime = '16:30'#为了使YiQingTongK=1
successCount = 0 #记录成功个数
failCount = 0
def YQsubmit(name,pushType,pushId,cookie,message):
    #pushType:1是server酱 2是测试号
    global successCount
    global failCount
    attemNumber = 0#尝试次数
    while(True):
        tmpres = os.popen('curl -H \'Host: zhxy.tjnu.edu.cn\' -H \'XPS-Token: B69C6B37B9B91573C65E0D7EEA950A46006672ECC83F91A8BC9C82F5D58C41C6A310FBBAE437FEECC01B35ED2EEE190AF5385F0F581C5803\' -H \'Accept: application/json, text/plain, */*\' -H \'Accept-Language: zh-cn\' -H \'' \
            'XPS-UserId: '+name+'\' -H \'Content-Type: application/x-www-form-urlencoded; charset=UTF-8\' -H \'Origin: http://zhxy.tjnu.edu.cn\' -H \'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) wxwork/3.0.24 (MicroMessenger/6.2) WeChat/2.0.4\' -H \'XPS-UserToken: B69C6B37B9B91573C65E0D7EEA950A46006672ECC83F91A8BC9C82F5D58C41C6A310FBBAE437FEECC01B35ED2EEE190AF5385F0F581C5803\' -H \'XPS-LoginType: WEIXIN\' -H \'Referer: http://zhxy.tjnu.edu.cn/h5/epidemic-report/index.html\' -H \'XPS-ClientCode: tjsd\' -H \'' \
                'Cookie: '+cookie+'\' ' \
                    '--data-binary "'+'items='+urllib.parse.quote(message)+'" --compressed \'http://zhxy.tjnu.edu.cn/app/health/submitSurvey\'').readlines()
        print(tmpres)
        if('1' in str(tmpres)):
            #成功 消息推送微信公众号
            weixinPush(pushType,pushId,"疫情通提交成功")
            successCount += 1
            break
        else:
            if(attemNumber<3):
                weixinPush(pushType,pushId,'疫情通提交失败'+',尝试'+str(abs(attemNumber)))
                time.sleep(10)
                attemNumber+=1
            else:
                #尝试次数过多
                weixinPush(pushType,pushId,"疫情通提交失败，不再尝试，请手动提交")
                failCount += 1
                break

def TWsubmit(name,pushType,pushId,cookie,temType,temperature):
    #pushType:1是server酱 2是测试号
    global successCount
    global failCount
    attemNumber = 0#尝试次数
    while(True):
        tmpres = os.popen('curl -H \'Host: zhxy.tjnu.edu.cn\' -H \'XPS-Token: B69C6B37B9B91573B1D4C7C55C8340562900314EF1998B90D50AAFE8D3ADE92C6A59B5DA5C0B3FC3D9751C81B36ABF5B5928D9C7CADDD205\' -H \'Accept: application/json, text/plain, */*\' -H \'Accept-Language: zh-cn\' -H \'' \
            'XPS-UserId: '+str(name)+'\' -H \'Content-Type: application/x-www-form-urlencoded; charset=UTF-8\' -H \'Origin: http://zhxy.tjnu.edu.cn\' -H \'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) wxwork/3.0.24 (MicroMessenger/6.2) WeChat/2.0.4\' -H \'XPS-UserToken: B69C6B37B9B91573B1D4C7C55C8340562900314EF1998B90D50AAFE8D3ADE92C6A59B5DA5C0B3FC3D9751C81B36ABF5B5928D9C7CADDD205\' -H \'XPS-LoginType: WEIXIN\' -H \'Referer: http://zhxy.tjnu.edu.cn/h5/temperature-report/index.html\' -H \'XPS-ClientCode: tjsd\' -H \'' \
                'Cookie: '+cookie+'\' ' \
                    '--data-binary "quantumId='+str(temType)+'&temperature='+str(temperature)+'" --compressed \'http://zhxy.tjnu.edu.cn/app/bodyTemperature/update\'').readlines()
        print(tmpres)
        if('1' in str(tmpres)):
            #成功 消息推送微信公众号
            weixinPush(pushType,pushId,"体温提交成功")
            successCount += 1
            break
        else:
            if(attemNumber<3):
                weixinPush(pushType,pushId,'体温提交失败'+',尝试'+str(abs(attemNumber)))
                time.sleep(10)
                attemNumber+=1
            else:
                #尝试次数过多
                weixinPush(pushType,pushId,"体温提交失败，不再尝试，请手动提交")
                failCount += 1
                break


def weixinPush(pushType,pushId,text):#pushType:1是server酱 2是测试号
    # if(str(pushType) == '1'):
    url = "https://sc.ftqq.com/"+pushId+".send?text="+str(random.randint(0,100))+quote(text[0:100])
    response = urllib.request.urlopen(url)
    data = response.read().decode("utf-8")
    print(data)
    # else:
    #     url = 'curl -X POST \'http://'+ipAdress+'/push\' -H \'content-type: application/json\' -d \'{ "channelName": "'+quote(pushId)+'", "text": "'+text[0:100]+'" }\''
    #     print(url)
    #     tmpres = os.popen(url).readlines()
    #     print(tmpres)

def TWsubmitInit(temType):
    # 打开数据库连接
    global ipAdress
    global DBUser
    global DBPassword
    global DataBase
    db = pymysql.connect(ipAdress, DBUser,
                DBPassword, DataBase, charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    sql = "SELECT * FROM `userinfo`"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            try:
                id2 = row[0]
                print(id2)
                name = row[1]#用户的微信id
                #password = row[2]
                pushType = row[3]
                pushId = row[4]
                cookie = row[5]
                #message = row[6]
                # 打印结果
                # print("id=%s,name=%s,password=%s,pushType=%s,pushId=%s,cookie=%s,message=%s" %
                #     (id, name, password, pushType, pushId, cookie, message))
                TWsubmit(name,pushType,pushId,cookie,temType,'36.3')
                time.sleep(10)
            except BaseException as Argument:
                weixinPush(1,myPushId,'在遍历每个数据的时候出现了一次异常，'+str(Argument))
    except BaseException as Argument:
        weixinPush(1,myPushId,'Error: unable to fecth data'+str(Argument))
    finally:
        db.close()
def YQsubmitInit():
    global ipAdress
    global DBUser
    global DBPassword
    global DataBase
    # 打开数据库连接
    db = pymysql.connect(ipAdress, DBUser,
                DBPassword, DataBase, charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    sql = "SELECT * FROM `userinfo`"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            try:
                #id = row[0]
                # if(str(id) == '6'):
                #     raise Exception("抛出一个异常")
                name = row[1]#用户的微信id
                #password = row[2]
                pushType = row[3]
                pushId = row[4]
                cookie = row[5]
                message = row[6]
                # 打印结果
                # print("id=%s,name=%s,password=%s,pushType=%s,pushId=%s,cookie=%s,message=%s" %
                #     (id, name, password, pushType, pushId, cookie, message))
                YQsubmit(name,pushType,pushId,cookie,message)
                time.sleep(10)
            except BaseException as Argument:
                weixinPush(1,myPushId,'在遍历每个数据的时候出现了一次异常，'+str(Argument))
    except BaseException as Argument:
        weixinPush(1,myPushId,'Error: unable to fecth data'+str(Argument))
    finally:
        db.close()
def main():
    global morningK
    global noneK
    global nightK
    global YiQingTongK
    global myPushId
    global successCount
    global failCount
    while (True):   
        try:
            # 格式化h:m形式
            localTime = time.strftime("%H:%M", time.localtime())
            if(localTime > nightStartTime and localTime < nightEndTime and nightK <= 0):#晚上
                #晚上 体温
                morningK = 0#把morning标记为0 在明天早上就可以自动提交
                noneK = 0
                YiQingTongK = 0#让第二天的疫情通能正常运行
                successCount = 0#请0
                failCount = 0
                TWsubmitInit('10')
                nightK = 1#一天只提交一次
                weixinPush('1',myPushId,'晚上成功'+str(successCount)+',失败'+str(failCount))
            elif(localTime > noneStartTime and localTime < noneEndTime and noneK<=0):
                #中午
                morningK = 0
                nightK = 0
                successCount = 0#请0
                failCount = 0
                TWsubmitInit('9')
                noneK = 1
                weixinPush('1',myPushId,'中午成功'+str(successCount)+',失败'+str(failCount))
            elif(localTime > morningStartTime and localTime < morningEndTime and morningK<=0):
                # moring
                noneK = 0
                nightK = 0
                successCount = 0#请0
                failCount = 0
                TWsubmitInit('1')
                morningK = 1
                weixinPush('1',myPushId,'早上成功'+str(successCount)+',失败'+str(failCount))
            if(localTime > YQTStartTime and localTime < YQTEndTime and YiQingTongK <= 0):
                #疫情通
                successCount = 0#请0
                failCount = 0
                YQsubmitInit()
                YiQingTongK = 1
                weixinPush('1',myPushId,'疫情通成功'+str(successCount)+',失败'+str(failCount))
            time.sleep(5)
        except BaseException as Argument:
            weixinPush('1',myPushId,'可能是时间获取错误或数据库连接错误，'+str(Argument))




if __name__ == "__main__":
    try:
        main()
    except BaseException as Argument:
        #出现致命错误 程序要退出了
        weixinPush(1,myPushId,'程序退出'+str(Argument))


