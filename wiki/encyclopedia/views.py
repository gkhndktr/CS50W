from typing import KeysView
from django.forms.forms import Form
from django.http.request import HttpRequest
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.utils.html import format_html
from . import util
import markdown2
from markdown2 import Markdown
import re
from django import forms
from django.http import HttpResponseRedirect
import random

markdowner = Markdown()

class NameForm(forms.Form):
    file_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your content', 'style': 'height: 300px;','class': 'form-control'}) )

# Home button directs to this function via urls.py
def index(request):
    # lists all entries in the entries directory
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# If path wiki/title, below func runs.
def title(request,file_name):
    if not util.get_entry(file_name):
        error="The page you are looking for does not exist. Please click below to create a new page."
        return render(request, "encyclopedia/error.html",{"content":error})

    content=markdowner.convert(util.get_entry(file_name))
    if request.method == 'GET':
        return render(request, "encyclopedia/title.html",{"content":content,"file_name":file_name})


# Gets query name from search bar.
# If name in the entries render title.html
# else returns possible entries with searchPage.html
def query(request):
    query = request.GET.get('query').lower()
    print(query)
    results=[]
    for i in util.list_entries():
        if query ==i.lower():
            markdowned=markdowner.convert(util.get_entry(i))
            print(markdowned)
            return render(request, "encyclopedia/title.html",{"content":markdowned})   
        elif query in i.lower():
            results.append(i)
    else:
        return render(request, "encyclopedia/searchPage.html",{"results":results})

def create(request):
    if request.method == 'GET':
        form = NameForm()
        return render(request, "encyclopedia/create.html", {'form':form})

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            file_name= form.cleaned_data['file_name']
            content=form.cleaned_data['content'].lstrip("\n")
            if util.get_entry(file_name):
                error=f"Page already exist. {file_name} to go to page"
                form = NameForm()
                return render(request, "encyclopedia/create.html", {'form':form,"error":error,"file_name":file_name})
            else:
                util.save_entry(file_name, content)
                return render(request , "encyclopedia/title.html",{"file_name": file_name,"content":content} )

def edit(request,file_name):
    if request.method == 'GET':
        # content=markdowner.convert(util.get_entry(name))
        content=util.get_entry(file_name)
        # check whether it's valid:
        form = NameForm(initial={'file_name': file_name,"content":content})

        return render(request, "encyclopedia/edit.html", {"form": form})

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            file_name= form.cleaned_data['file_name']
            content=form.cleaned_data['content'].strip()
            util.save_entry(file_name, content)
            return redirect(f'/wiki/{file_name}')
def bring(request):
    file_name= random.choice(util.list_entries())
    return redirect('file_name', file_name=file_name)

