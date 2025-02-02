from django.http.response import JsonResponse
from lh3.api import *
from dashboard.utils.utils import (
    soft_anonimyzation, Chats
)
from datetime import datetime, timedelta
from django.shortcuts import render 
from dateutil.parser import parse

from dashboard.utils.daily_report import real_report
from dashboard.utils.utils import helper_for_operator_assignments

import pathlib
from project_config.settings import BASE_DIR
from django.http import FileResponse
import pandas as pd
import json 
from datetime import timezone, datetime
import json
from os import path

def chord_diagram(request):
    """
    client = Client()
    today = datetime.today()
    chats = client.chats()
    chats = chats.list_day(year=2021, month=1, day=1, to="2021-04-11")
    df = pd.DataFrame(chats)
    """

    return render(request, 'chord_diagram.html')

def daily_report(request):
    today = datetime.today().strftime('%Y-%m-%d')

    filename = "daily-" + today + ".xlsx"
    filepath = str(pathlib.PurePath(BASE_DIR, "tmp_file", filename))
    
    df = real_report()
    #Create file using the UTILS functions
    df.to_excel(filepath, index=False)

    #TODO: Create this report using a cronjob
    return FileResponse(open(filepath, 'rb'), as_attachment=True, filename=filename)


def pivotTableOperatorAssignment(request):
    assignments = helper_for_operator_assignments()
    
    context = {
        'schools': assignments
    }

    df = pd.DataFrame(assignments)
    df['operator_copy'] = df['operator']

    filename = "operator.xlsx"
    filepath = str(pathlib.PurePath(BASE_DIR, "tmp_file", filename))

    writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.save() 

    #return JsonResponse(context, safe=False)
    return render(request, 'pivot.html', context)


def download_excel_file_Operator_Assignment(request):
    
    filename = "operator.xlsx"
    filepath = str(pathlib.PurePath(BASE_DIR, "tmp_file", filename))
    
    from os import path
    if path.exists(filepath):
        print('file exist in : ' + filepath)
        return FileResponse(open(filepath, 'rb'), as_attachment=True, filename=filename)
    else:
        assignments = helper_for_operator_assignments()

        df = pd.DataFrame(assignments)
        df['operator_copy'] = df['operator']

        filename = "operator.xlsx"
        filepath = str(pathlib.PurePath(BASE_DIR, "tmp_file", filename))

        writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
        df.to_excel(writer, index=False)
        writer.save() 

    #TODO: Create this report using a cronjob
    return FileResponse(open(filepath, 'rb'), as_attachment=True, filename=filename)


def get_unanswered_chats(request, *args, **kwargs):
    client = Client()
    today = datetime.today()
    chats = client.chats()
    last10days = today - timedelta(days=10)

    to_date = str(last10days.year) + "-" + '{:02d}'.format(last10days.month)  + "-" + str(last10days.day)
    all_chats = chats.list_day(year=today.year, month=today.month, day=today.day, to=to_date)
    unanswered=list()
    for chat in all_chats:
        if chat.get('operator')== None:
            unanswered.append(chat)

    #return JsonResponse(chats, safe=False)
    heatmap = [parse(chat.get('started')).replace(tzinfo=timezone.utc).timestamp() for chat in unanswered]
    counter=  {x:heatmap.count(x) for x in heatmap}
    heatmap_chats = json.dumps(counter)
    username= "Unanswered"  
    current_year = 'Last 10 days'

    unanswered = [Chats(chat) for chat in unanswered]
    return render(request, "results/chats.html", {'object_list':unanswered, 
        'heatmap_chats':heatmap_chats, 'username':username, 'current_year':current_year})


def pivotTableChatAnsweredByOperator(request):
    client = Client()
    chats = client.chats()

    today = datetime.today()
    yesterday = today - timedelta(days=3)

    chats = client.chats().list_day(year=2021, month=4, day=1, to="2021-05-18")[0:200]
    chats_initital = [Chats(chat) for chat in chats]

    chats_initital = [{'queue': s.queue, 'school': s.school, 'year': parse(s.started).year, 'month': parse(s.started).strftime('%B'), 'operator': s.operator } for s in chats_initital]
    
    breakpoint()
    operators = [chat.get('operator') for chat in chats_initital]
    queues = [chat.get('queue') for chat in chats]
    context = {
        'schools': chats_initital
        
    }
    return render(request, 'pivot.html', context)

