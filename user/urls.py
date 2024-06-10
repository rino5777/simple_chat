from django.urls import path
from .views import logoutuser, RegisterUserView, Logining


app_name = 'user'

urlpatterns = [

    path('logout/', logoutuser ,name='logout'),
    path('signup/', RegisterUserView.as_view() ,name='signup'),
    path('login/', Logining.as_view() ,name='login'),
    

    
]