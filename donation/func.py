# coding:utf-8
import time
import datetime
import urllib2
import os


false = 'false'
true = 'true'


def GetCurrentMonthDay(currentday):
    today = datetime.date.today()
    Year = int(today.year)
    Month = int(today.month)
    d1 = datetime.datetime(Year, Month, 1)
    if Month == 12:
        Month = 1
        Year += 1
    else:
        Month += 1
    d2 = datetime.datetime(Year, Month, 1)
    days = d2 - d1
    day = days.days
    return day


########################计算赛季第几天######################

def GetSeasondays():
    today = datetime.date.today()
    A = GetCurrentMonthDay(today)
    W = today.isoweekday()
    DD = today.day
    thismonth = datetime.date(today.year, today.month, 1)
    K = thismonth.isoweekday()
    if A - DD + W <= 7:
        day = W
    else:
        day = K + DD - 1
    return day


######################计算赛季剩余几天######################

def GetDaysRemaining():
    Count = 0
    today = datetime.date.today()
    delta = datetime.timedelta(days=1)
    while today.isoweekday() != 7:
        today += delta
        Count += 1
    month = today.month
    while today.month == month:
        delta = datetime.timedelta(days=7)
        today += delta
        if today.month == month:
            Count += 7
    return Count


def role_re(role, donations, donationsReceived):  # 写死捐收合格情况
    if role == 'leader':
        if donations < 2000:
            re_check = '不合格'.decode('utf8')
        else:
            re_check = '合格'.decode('utf8')
        res = '首领'.decode('utf8')
    elif role == 'coLeader':
        if donations < 2000:
            re_check = '不合格'.decode('utf8')
        else:
            re_check = '合格'.decode('utf8')
        res = '副首领'.decode('utf8')
    elif role == 'admin':
        if donations < 1000:
            re_check = '不合格'.decode('utf8')
        else:
            re_check = '合格'.decode('utf8')
        res = '长老'.decode('utf8')
    else:
        if (donations + donationsReceived) < 1000:
            re_check = '不合格'.decode('utf8')
        else:
            re_check = '合格'.decode('utf8')
        res = '成员'.decode('utf8')
    return [res, re_check]


def wclan(clan_id):  # 通过部落接口，获取原数据
    try:
        request = urllib2.Request("http://94.191.30.195:3000/api/clans/tag/%s" % clan_id)
        response = urllib2.urlopen(request)
        html = response.read()
        # w=open('%s.txt'%clan_id,'w').write('%s'%html)
        return html
    except:
        return 0


def member_detail(member_id):  # 通过menber接口返回成员大本营等级
    try:
        request = urllib2.Request("http://94.191.30.195:3000/api/player/tag/%s" % member_id)
        response = urllib2.urlopen(request)
        html = eval(response.read())
        townHallLevel = html['townHallLevel']

        return townHallLevel
    except Exception, e:
        return e


def add_clan(clan_id):  # 把部落数据添加到列表，以供html读取
    now_time = time.time()
    try:
        revise_time = os.path.getmtime('clans/%s.txt' % clan_id)
    except:
        revise_time = 0
    if now_time - revise_time > 120:  # 若修改时间距离现在大于120秒，则重新获取数据
        # print '大于120秒'
        result = wclan(clan_id)
        if result:
            d = eval(result)
            menbers_list = []
            j = 0
            try:
                townHallLevel_revise_time = os.path.getmtime('clans/%s_townHallLevel.txt' % clan_id)
            except:
                townHallLevel_revise_time = 0
            if now_time - townHallLevel_revise_time < 86400:  # 若修改时间距离现在少于1天，则读取原来大本营等级数据
                townHallLevel_list = eval(open('clans/%s_townHallLevel.txt' % clan_id).read())

                for i in d['memberList']:
                    donations = i["donations"]  # 捐数量
                    donationsReceived = i["donationsReceived"]  # 收数量
                    donations_dif = donations + donationsReceived  # 捐收和
                    tag = i['tag'].replace('#', '')  # 成员ID
                    townHallLevel = townHallLevel_list[tag]  ###
                    j += 1
                    menbers_list.append(
                        [j, i["name"], role_re(i["role"], donations, donationsReceived), donations, donationsReceived,
                         donations_dif, townHallLevel])

            else:  # 若修改时间距离现在大于1天，则重新获取大本营等级数据
                townHallLevel_list = {}
                for i in d['memberList']:
                    donations = i["donations"]  # 捐数量
                    donationsReceived = i["donationsReceived"]  # 收数量
                    donations_dif = donations + donationsReceived  # 捐收和
                    tag = i['tag'].replace('#', '')  # 成员ID
                    townHallLevel = member_detail(tag)
                    j += 1
                    townHallLevel_list[tag] = townHallLevel
                    menbers_list.append(
                        [j, i["name"], role_re(i["role"], donations, donationsReceived), donations, donationsReceived,
                         donations_dif, townHallLevel])
                w = open('clans/%s_townHallLevel.txt' % clan_id, 'w')
                w.write('%s' % townHallLevel_list)
                w.close()
                # open(r'clans/%s_townHallLevel.txt' % clan_id, 'w').write('%s' % townHallLevel_list)
        else:
            menbers_list = []

        w = open('clans/%s.txt' % clan_id, 'w')
        w.write('%s' % menbers_list)
        w.close()
        # open(r'clans/%s.txt' % clan_id, 'w').write('%s' % menbers_list)
        return menbers_list

    else:  # 否则读取上一次获取的数据
        # print '少于120秒'
        menbers_list = eval(open('clans/%s.txt' % clan_id).read())
        return menbers_list