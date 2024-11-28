from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .models import Dreamer, Dream
from django.contrib import messages
from .forms import DreamerForm
# Create your views here.



def index(request):
    return render(request, 'hopesdreams/base_template.html')

def listdreamer(request):
    dreamerlist = Dreamer.objects.all()
    context = {'dreamerlist': dreamerlist}
    return render(request, 'hopesdreams/dreamer_list.html', context)

def adddreamer(request):
    if request.method == 'GET':
        cf = DreamerForm()
    elif request.method == 'POST':
        cf = DreamerForm(request.POST)
        if cf.is_valid():
            cf.save()
            return redirect('hopesdreams:dreamer-list')
    context = {'form': cf, 'actionname': 'Add'}
    return render(request, 'hopesdreams/dreamer_form.html', context)




def detaildreamer(request, pk):
    c = Dreamer.objects.get(id = pk)
    context = {'dreamer': c}
    return render(request, 'hopesdreams/dreamer_detail.html', context)