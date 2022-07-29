from django.urls import path 
from . import views 

urlpatterns = [
    path('',views.index,name='index'),
    path('callback/',views.retrieveCallbackCode,name="retrieveCallbackCode"),
    path('schedule',views.displayMeeting,name='displayMeeting'),
    path('schedule/create/',views.createMeeting,name='createMeeting'),
    #path('schedule/display',views.tempDisplay,name='tempDisplay')
]