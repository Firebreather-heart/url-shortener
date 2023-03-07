from django.forms import ModelForm
from .models import UrlHolder
from django.contrib.auth.models  import User 
from django.contrib.auth.forms import UserChangeForm,UserCreationForm

class UrlForm(ModelForm):
    class Meta:
        model = UrlHolder
        fields = ['destination', 'custom_addr']
    
    def save(self, commit: bool = True):
        #urlobj = super().save(commit = False)
        self.cleaned_data['custom_addr'] = self.cleaned_data['custom_addr'].lower()
        return super().save(commit)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email',)