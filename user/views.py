
from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import  logout
from .forms import RegisterUserForm, LoginUserForm, ChangeUserInfoForm, CreateRoom
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.
class RegisterUserView(CreateView):
    model = User
    template_name = 'autentication/signup.html'
    form_class = RegisterUserForm
    
    success_url = reverse_lazy('user:login')

    def get(self, request, *args, **kwargs):
        
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

class Logining(LoginView):
    template_name = 'autentication/login.html'
    form_class = LoginUserForm
    success_url = reverse_lazy('chat:home')
    
    def get_success_url(self):
        return self.success_url





def logoutuser(request):
    logout(request)
    return redirect('user:login')


# def create_room(request):
#     if request.method == 'POST':
#         form_room = CreateRoom(request.POST)
#         if form_room.is_valid():
#             room = form_room.save(commit=False)
#             room.save() 
#             room.users.add(request.user)
#             room.save() 
#             return redirect('room_success') 
#     else:
#         form_room = CreateRoom()

#     return render(request, 'index.html', {'form_room': form_room})
