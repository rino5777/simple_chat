from django.urls import path
from .views import Main, room, delete_room, ChangeUserInfoView, MainChangeUserInfoView, create_room, JoinRoomView

app_name = 'chat'

urlpatterns = [

    
    path('', MainChangeUserInfoView.as_view() ,name='home'),
    path('profile/', ChangeUserInfoView.as_view() ,name='profile'),
    path('create/', create_room ,name='create'),
    path('<slug:slug>/', room, name='room'),
    path('join-room/<slug:slug>/', JoinRoomView.as_view(), name='join-room'),
    

]