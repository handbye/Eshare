from django.shortcuts import render
from . import  models
import datetime,requests
from django.contrib.sessions.models import Session

def index(request):
    total = models.Asset.objects.count()
    upline = models.Asset.objects.filter(status=0).count()
    offline = models.Asset.objects.filter(status=1).count()
    breakdown = models.Asset.objects.filter(status=2).count()
    warning = models.Asset.objects.filter(status=3).count()
    other = total - upline - offline - breakdown - warning

    server_number = models.Server.objects.count()
    network_number = models.NetworkDevice.objects.count()
    storage_number = models.StorageDevice.objects.count()
    business_number = models.BusinessUnit.objects.count()

    CAS_number = models.Server.objects.filter(sub_asset_type=0).count()
    UIS_number = models.Server.objects.filter(sub_asset_type=1).count()
    CloudOs_number = models.Server.objects.filter(sub_asset_type=2).count()
    Class_number = models.Server.objects.filter(sub_asset_type=3).count()
    other_server_number = server_number-CAS_number-UIS_number-Class_number-CloudOs_number

    today =  datetime.datetime.now()
    timeDict=[]
    timeDict.append(today.strftime('%Y-%m-%d'))
    for i in range(1,5):
        yesterday = today - datetime.timedelta(days=i)
        timeDict.append(yesterday.strftime('%Y-%m-%d'))
    t1 = timeDict[-1]
    t2 = timeDict[-2]
    t3 = timeDict[-3]
    t4 = timeDict[-4]
    t5 = timeDict[-5]

    # login_time = models.User.objects.get(username='admin').last_login

    user_count1 = models.User.objects.filter(last_login__range=(t1,t2)).count()
    user_count2 = models.User.objects.filter(last_login__range=(t2,t3)).count()
    user_count3 = models.User.objects.filter(last_login__range=(t3,t4)).count()
    user_count4 = models.User.objects.filter(last_login__range=(t4,t5)).count()
    user_count5 = models.User.objects.filter(last_login__gte=t5).count()

    # 获取在线人数
    sessions = Session.objects.filter(expire_date__gte=datetime.datetime.now())
    uid_list = []
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id',None))
    user_names = models.User.objects.filter(id__in=uid_list)
    user_online_number = models.User.objects.filter(id__in=uid_list).count() #在线用户数

    #以下这条数据不知道怎么传到前台，待定
    # online_users = models.User.objects.filter(id__in=uid_list) #在线用户

    user_total_number = models.User.objects.all().count()
    user_offline_number = user_total_number-user_online_number

    return render(request,'cloud/index.html',locals())


def datatables(request):
    assets = models.Asset.objects.all()

    #以下代码可以探测设备状态
    for a in assets:
        if a.status ==1 or a.status==2:
            url = 'http://'+a.manage_ip+':'+'8080'
            try:
                r = requests.get(url,timeout=0.2)
                if r.status_code==200:
                     models.Asset.objects.filter(manage_ip=a.manage_ip).update(status=0)
            except requests.exceptions.RequestException:
                pass
            continue
        else:
            url = 'http://' + a.manage_ip + ':' + '8080'
            try:
                r = requests.get(url, timeout=0.2)
                if r.status_code==200:
                    pass
            except requests.exceptions.RequestException :
                models.Asset.objects.filter(manage_ip=a.manage_ip).update(status=2)
                pass
            continue
    return render(request, 'cloud/datatables.html', locals())