from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView, View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Room, Message
from django.utils.decorators import method_decorator
from user.forms import ChangeUserInfoForm, CreateRoom, UploadImageForm, RoomPasswordForm
from .models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
# Create your views here.



class Main(TemplateView):
    template_name = 'index.html'
    change_info_form = ChangeUserInfoForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse_lazy('user:signup'))
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(login_required)
    def get(self, request):
        info_form = self.change_info_form()
        rooms = Room.objects.all()
        if request.method == 'POST':
            room = Room(name=str(len(rooms) + 1), slug=str(len(rooms) + 1))
            room.save()
            return redirect('home')
        return render(request, self.template_name, {'rooms': rooms, 'info_form':info_form})
    






def delete_room(request, id):
    del_room = Room.objects.get(id=id)
    del_room.delete()

    return redirect('rooms')


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin,
                                              UpdateView):
    model = User
    template_name = 'profile/profile.html'
    form_class = ChangeUserInfoForm
    image_form = UploadImageForm
    success_url = reverse_lazy('chat:profile')
    success_message = 'Данные пользователя изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)  

    def get(self, request, *args, **kwargs):
        info_form = self.form_class(instance=self.get_object())
        avatar_form = self.image_form(instance=self.get_object())
        rooms = Room.objects.all()
        return render(request, self.template_name, {'rooms': rooms, 'info_form': info_form, "avatar_form": avatar_form })

    def post(self, request, *args, **kwargs):

        info_form = self.form_class(request.POST, instance=self.get_object()) 
        avatar_form = self.image_form(request.POST, request.FILES, instance=self.get_object())
        info_form_valid = info_form.is_valid()
        avatar_form_valid = avatar_form.is_valid()

        if not info_form_valid:
            print("Info form errors:", info_form.errors)
        if not avatar_form_valid:
            print("Avatar form errors:", avatar_form.errors)

      

        if info_form.is_valid():
            print('f1')
            info_form.save()
            return redirect(self.success_url)
        elif avatar_form.is_valid():
            print('f2')
            avatar_form.save()
            return redirect(self.success_url)
        else:
            rooms = Room.objects.all()
            return render(request, self.template_name, {'rooms': rooms, 'info_form': info_form, "avatar_form":avatar_form})  
    

# ---------------------------------------------------------------------------------------------------------

# class MainChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, TemplateView, UpdateView):
#     model = User
#     template_name = 'index.html'
#     form_class = ChangeUserInfoForm
#     success_url = reverse_lazy('chat:home')
#     success_message = 'Данные пользователя изменены'

#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return redirect(reverse_lazy('user:signup'))
#         return super().dispatch(request, *args, **kwargs)

#     def setup(self, request, *args, **kwargs):
#         self.user_id = request.user.pk
#         return super().setup(request, *args, **kwargs)

#     def get_object(self, queryset=None):
#         if not queryset:
#             queryset = self.get_queryset()
#         return get_object_or_404(queryset, pk=self.user_id)

#     def get_queryset(self):
#         return User.objects.filter(pk=self.request.user.pk)

#     def get(self, request, *args, **kwargs):
#         info_form = self.form_class(instance=self.get_object())
#         rooms = Room.objects.all()
#         return render(request, self.template_name, {'rooms': rooms, 'info_form': info_form})

#     def post(self, request, *args, **kwargs):

#         info_form = self.form_class(request.POST, instance=self.get_object())
#         if info_form.is_valid():
#             info_form.save()
#             return redirect(self.success_url)
#         else:
#             rooms = Room.objects.all()
#             return render(request, self.template_name, {'rooms': rooms, 'info_form': info_form})
        

def create_room(request):
    if request.method == 'POST':
        form_room = CreateRoom(request.POST)
        if form_room.is_valid():
            
            room = form_room.save(commit=False) 
            room.save() 
            room.users.add(request.user) 
            room.save() 
            return redirect('chat:home') 
    else:
        form_room = CreateRoom() 
    return render(request, 'create_room_form.html', {'form_room': form_room})
        


@login_required
def room(request, slug):
    room = get_object_or_404(Room, slug=slug)
    rooms = Room.objects.all()
    messages = Message.objects.filter(room=room)[:25]
    info_form = ChangeUserInfoForm
    users_in_room = room.users.all()
    guest = ''
    for user in users_in_room:
        if request.user.email != user.email:
            guest = user
    
    return render(request, 'chat/chat-1.html', {'room': room, 'rooms': rooms, 'messages': messages, 'info_form': info_form, 'guest':guest})

# @login_required
# def join_room(request, slug):
#     room = get_object_or_404(Room, slug=slug)
#     if request.method == 'POST':
#         roompasswordform = RoomPasswordForm(request.POST)
#         if roompasswordform.is_valid():
#             password = roompasswordform.cleaned_data['password']
#             if room.check_password(password):  # Проверка пароля, если он установлен
#                 room.users.add(request.user)
#                 return redirect('chat:room', slug=room.slug)  # Переход в комнату после успешного ввода пароля
#             else:
#                 roompasswordform.add_error('password', 'Incorrect password')
#     else:
#         roompasswordform = RoomPasswordForm()
#     return render(request, 'index.html', {'form': roompasswordform, 'room': room})


class MainChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, TemplateView, UpdateView):
    model = User
    template_name = 'index.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('chat:home')
    success_message = 'Данные пользователя изменены'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse_lazy('user:signup'))
        return super().dispatch(request, *args, **kwargs)

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get(self, request, *args, **kwargs):
        info_form = self.form_class(instance=self.get_object())
        rooms = Room.objects.all()
        return render(request, self.template_name, {'rooms': rooms, 'info_form': info_form})

    def post(self, request, *args, **kwargs):
        info_form = self.form_class(request.POST, instance=self.get_object())
        if info_form.is_valid():
            info_form.save()
            return redirect(self.success_url)
        else:
            rooms = Room.objects.all()
            return render(request, self.template_name, {'rooms': rooms, 'info_form': info_form})

class JoinRoomView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/pass.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['roompasswordform'] = RoomPasswordForm()
        context['room'] = get_object_or_404(Room, slug=self.kwargs['slug'])
        return context

    def post(self, request, slug):
        room = get_object_or_404(Room, slug=slug)
        roompasswordform = RoomPasswordForm(request.POST)
        if roompasswordform.is_valid():
            password = roompasswordform.cleaned_data['password']
            if room.check_password(password):  
                room.users.add(request.user)
                return redirect('chat:room', slug=room.slug)  
            else:
                roompasswordform.add_error('password', 'Incorrect password')
        return render(request, self.template_name, {'roompasswordform': roompasswordform, 'room': room})