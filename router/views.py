from django.shortcuts import  render,redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError
from .models import UrlHolder, Metrics
from .forms import UrlForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

from django.views import generic
from .forms import CustomUserCreationForm

class SignupPageView(generic.CreateView):
    form_class = CustomUserCreationForm
    #success_url = reverse_lazy('home')
    template_name = 'signup.html'

    def get_success_url(self):
        print('sucess!!')
        return reverse_lazy('home')

@login_required 
def index(request):
    urlbucket = UrlHolder.objects.filter(owner = request.user)
    if request.method == 'POST':
        urlform = UrlForm(request.POST)
        user = request.user
        if urlform.is_valid():
            urlform = urlform.save(commit = False)
            original = urlform.destination.lower()
            custom = urlform.custom_addr.lower()
            try:
                metrics = Metrics()
                metrics.save()
                new_url = UrlHolder(owner = user, destination=original, custom_addr = custom, metrics = metrics)
                new_url.save()
                
            except IntegrityError:
                print('error')
                messages.add_message(request, messages.ERROR, 'The url already exists')
            else:
                print('success')
                messages.add_message(request, messages.SUCCESS, 'url created successfully')
        return redirect('home')
    else:
        urlform = UrlForm()
    return render(request, 'index.html', {'form': urlform, 'urls':urlbucket})
    

def route(request, arg):
    url = get_object_or_404(UrlHolder, custom_addr = arg)
    dest = url.destination
    metrics = url.metrics
    metrics = metrics.new_visit()
    print(metrics.visits)
    metrics.save()
    return redirect(dest)

