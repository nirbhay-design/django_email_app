from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('login/<str:email_id>/',views.mainapp,name='main app window'),
    path('login/<str:email_id>/inbox/',views.inbox,name='main app window'),
    path('login/<str:email_id>/sent/',views.sent,name='main app window'),
    path('login/<str:email_id>/deleted/',views.deleted,name='main app window'),
    path('login/<str:email_id>/compose/',views.compose,name='main app window'),
    path('login/<str:email_id>/inbox/read/<int:id>/',views.InboxReadMail,name='main app window'),
    path('login/<str:email_id>/sent/read/<int:id>/',views.SentReadMail,name='main app window'),
    path('login/<str:email_id>/deleted/read/<int:id>/',views.DeleteReadMail,name='main app window'),
    path('login/<str:email_id>/inbox/delete/<int:id>/',views.DeleteMail,name='main app window'),
]

