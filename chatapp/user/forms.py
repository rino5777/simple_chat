from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from .models import User
from chat.models import Room
from django.contrib.auth.forms import AuthenticationForm
from django.utils.text import slugify


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(
        required=True, 
        label='Адрес электронной почты',
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-md', 
            'placeholder': 'Введите ваш email', 
            'id': 'email'
        })
    )
    password1 = forms.CharField(
        label='Пароль', 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-md', 
            'placeholder': 'Введите ваш пароль', 
            'id': 'password1'
        }),
        help_text=password_validation.password_validators_help_text_html()
    )
    password2 = forms.CharField(
        label='Пароль (повторно)', 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-md', 
            'placeholder': 'Введите ваш пароль еще раз', 
            'id': 'password2'
        }),

        help_text='Введите тот же самый пароль еще раз для проверки'
    )

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            # проверка на безопасность 
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
              'Введенные пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        user.is_activated = False
        if commit:
            user.save()
        
        return user

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):

    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-md', 
                                        'placeholder': 'Enter your email', 
                                        'id': 'email'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-md', 
                                          'placeholder': 'Введите ваш пароль', 
                                          'id': 'password'})
    )


class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control form-control-md', 
                                        'placeholder': 'Enter your email', 
                                        'id': 'emailAddress'}))

    class Meta:
        model = User
        fields = ( 'email',  )



class CreateRoom(forms.ModelForm): 
#<input type="text" class="form-control form-control-md" id="inviteEmailAddress" placeholder="Name" value=""> 
    name = forms.CharField(
            widget=forms.TextInput(attrs={'class': 'form-control form-control-md', 
                                            'placeholder': 'room name', 
                                            'id': 'name'})
        )
    
    slug = forms.CharField(
            widget=forms.TextInput(attrs={'class': 'form-control form-control-md', 
                                            'placeholder': 'room name', 
                                            'id': 'slug'})
        )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-md', 
                                          'placeholder': 'Password', 
                                          'id': 'password'}),
        label="Password",
        required=False 
    )

    class Meta:
        model = Room
        fields = ('name', 'slug', 'password')

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        name = self.cleaned_data.get('name')
       
        if not slug:
            slug = slugify(name)
            original_slug = slug
            counter = 1

            while Room.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1

        return slug
       
class RoomPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-md', 
                                          'placeholder': 'Password', 
                                          'id': 'password'}),
        label="Password"
    )

   

class UploadImageForm(forms.ModelForm):
    avatar = forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Upload your avatar'})

    class Meta:
        model = User
        fields = ( 'avatar',  )