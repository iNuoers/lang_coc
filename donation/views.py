# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from func import *


def goto(request, clan_id):
    if clan_id == '':
        clan_id = 'V9QG2QP8'

    days = GetSeasondays()
    daysremaining = GetDaysRemaining()

    if clan_id != '':
        menbers_list = add_clan(clan_id)
    else:
        menbers_list = []
    context = {'menbers_list': menbers_list, 'clan_id': clan_id, 'days': days, 'daysremaining': daysremaining}
    return render(request, 'donation/index.html', context)


def done(request):
    clan_id = request.POST['clan_id']
    return HttpResponse(u"<html><head><meta http-equiv='Content-Type' content='text/html; charset=UTF-8'/>done~ \
        <script type=\"text/javascript\">window.setTimeout(\"location='/goto/%s/'\", 0);</script> </html>" % clan_id)
