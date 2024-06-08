from django.forms.widgets import ClearableFileInput

class CustomClearableFileInput(ClearableFileInput):
    template_name = 'profile/custom_clearable_file_input.html'