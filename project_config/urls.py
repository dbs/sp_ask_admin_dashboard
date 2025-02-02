"""seminar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.urls import re_path

from dashboard.views.views_api import (
    get_users, 
    get_queues, 
    get_profiles,
)

# API
urlpatterns = [
    path('users/', get_users, name='get_list_of_users'),
    path('queues/', get_queues, name='get_list_of_queues'),
    path('profiles/', get_profiles, name='get_list_of_profiles'),
   
]

# ASSIGNEE
from dashboard.views.views_assignee import (
    get_assignee_for_this_queue, 
)

urlpatterns += [
    path('assignee/<str:queue_name>', get_assignee_for_this_queue, name='get_list_of_assignee_for_this_queue'),
]

# HOMEPAGE
from dashboard.views.views_homepage import (
    get_operators_currently_online,
    get_total_for_this_day,
    get_total_for_this_month, 
    get_total_for_this_year,
    get_list_of_last_400_chats,
    get_total_chats_per_month_for_this_year,
    service_web,
    service_fr,
    service_sms,
    get_data_for_chart,
    get_data_for_users_currently_online_table,
    
)

urlpatterns += [
    path('get_table/', get_data_for_users_currently_online_table, name='get_data_for_users_currently_online_table'),
    path('current/', get_operators_currently_online, name='get_operators_currently_online'),
    path('today/', get_total_for_this_day, name='get_total_for_this_day'),
    path('thismonth/', get_total_for_this_month, name='get_total_for_this_month'),
    path('thisyear/', get_total_for_this_year, name='get_total_for_this_year'),
    path('sumthisyear/', get_total_chats_per_month_for_this_year, name='get_total_chats_per_month_for_this_year'),
    path('last400/', get_list_of_last_400_chats, name='get_list_of_last_400_chats'),
    path('service_web/', service_web, name='service_web'),
    path('service_sms/', service_sms, name='service_sms'),
    path('service_web/', service_fr, name='service_fr'),
    path('homepage/chart/', get_data_for_chart, name='get_data_for_chart'),
    
]


# SEARCH
from dashboard.views.views_search import (
    get_chats_for_this_user,
    get_chats_for_this_queue,
    get_this_profile,
    SearchProfileResultsView,
    get_chats_from_yesterday,
    get_chats_from_yesterday_from_mentees,
    get_chat_for_date_range,
    search_chats_with_this_guestID,
    SearchGuestResultsView,
    search_chats_within_2_hours,
    get_chats_from_yesterday_sample_size,
)

urlpatterns += [
    path('search/chats/with/this/guestID/<str:guest_id>', SearchGuestResultsView.as_view(), name='results_chats_with_this_guestID'),
    path('search/chats/with/this/guestID/', search_chats_with_this_guestID , name='search_chats_with_this_guestID'),

    path('search/chats/within/two/hours/<str:chat_id>', search_chats_within_2_hours, name='search_chats_within_2_hours'),
    path('search/chats/answered/by/this/users/<str:username>', get_chats_for_this_user, name='get_chats_for_this_user'),
    path('search/queues/<str:queue_name>', get_chats_for_this_queue, name='get_chats_for_this_queue'),
    path('search/profiles/<str:queue_id>', get_this_profile, name='get_this_profile'),
    path('resultsProfiles/', SearchProfileResultsView.as_view(), name='results_profiles'),
    path('yesterday/', get_chats_from_yesterday, name='get_chats_from_yesterday'),
    path('yesterday/sample/', get_chats_from_yesterday_sample_size, name='get_chats_from_yesterday_sample_size'),
    path('yesterday/from/mentees/', get_chats_from_yesterday_from_mentees, name='get_chats_from_yesterday_from_mentees'),
    path('chats/daterange/', get_chat_for_date_range, name='get_page_chat_for_date_range',),
    path(route='search/chats/in/date/range/', 
        view=get_chat_for_date_range, 
        name='search_chats_in_date_range', 
        kwargs={'view_filepath': 'report.views.chats_report.py'}),

]

# REPORT
from dashboard.views.views_report import (
    pivotTableOperatorAssignment,
    download_excel_file_Operator_Assignment,
    get_unanswered_chats,
    pivotTableChatAnsweredByOperator,
    daily_report,
    chord_diagram,

)

urlpatterns += [
    path('report/operator/assignment',  pivotTableOperatorAssignment, name='pivotTableOperatorAssignment'),
    path('download/report/operator/assignment',  download_excel_file_Operator_Assignment, name='download_excel_file_Operator_Assignment'),
    path('unanswered/', get_unanswered_chats, name='get_unanswered_chats'),
    path('pivot/table/chats/by/operator', pivotTableChatAnsweredByOperator, name='pivotTableChatAnsweredByOperator'),
    path('report/daily', daily_report, name='daily_report'),
    path('charts/chord_diagram', chord_diagram, name='chord_diagram'),


]

# SCHOOLS
from dashboard.views.views_search import (
    get_chats_for_this_school_using_an_username,
    get_chats_for_this_school_using_this_queue_name,
    get_chats_from_this_queue_using_only_the_queue_name,
)

urlpatterns += [
    path('search/chats/from/this/school/using/this/username/<str:username>', get_chats_for_this_school_using_an_username, name='get_chats_for_this_school_using_an_username'),
    path('search/chats/from/this/school/using/this/queue_name/<str:queue_name>', get_chats_for_this_school_using_this_queue_name, name='get_chats_for_this_school_using_this_queue_name'),
    path(
        route='search/chats/from/this/queue/using/only/the/queue_name/<str:queue_name>', 
            view=get_chats_from_this_queue_using_only_the_queue_name, 
            name='get_chats_from_this_queue_using_only_the_queue_name',
            kwargs={"view_filepath":"views.main.report_view.py"}
        ),

]

# TRANSCRIPTS
from dashboard.views.views_transcript import (
    get_transcript,
    download_transcript_in_html,
)

urlpatterns += [
    path('search/chat/transcript/<int:chat_id>', get_transcript, name='get_chat_transcript'),
    path('download/this/transcript/<int:chat_id>', download_transcript_in_html, name='download_transcript_in_html'),
]

#HOMEPAGE


from dashboard.views.views_homepage import (
    get_homepage,
)

urlpatterns += [
    path('', get_homepage, name='homepage', kwargs={'view_filepath': 'view.main.homepage.py'}),
]





#Surveys

#Reference Question
