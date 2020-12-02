from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import *
from . import util
import random

from markdown2 import Markdown

markdowner = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm(),
    })

def title(request, title):
    requested = util.get_entry(title)

    if requested is None:
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "form": SearchForm(),
        })

    else:
        return render(request, "encyclopedia/title.html", {
            "title": title,
            "torender": markdowner.convert(requested),
            "form": SearchForm(),
        })

def search(request, *args, **kwargs):
    matchList=[] 
    allentries = util.list_entries()
    if request.method == 'POST':
        data = SearchForm(request.POST)
        print("this is all entries", allentries)
        print("this is the data", data)
        ###if data != None:
        if data.is_valid():
            ##print(query)
            Q = data.cleaned_data["query"]
            for i in allentries:
                if i.lower() == Q.lower():                      
                    """result = util.get_entry(Q)
                    torender = markdowner.convert(result)
                    return render(request, "encyclopedia/title.html", {
                        'torender': torender,
                        'title': Q,
                        'form': SearchForm()
                        }) """### old code for review ###
                    return title(request, Q)
            else:
                matchList = list(filter(lambda x: Q.lower() in x.lower(), allentries)) 
                if len(matchList) > 0:
                    return render(request, "encyclopedia/partial_results.html", {
                        "results": matchList,
                        "form": SearchForm()  
                    })
                else:
                    print("we eneded up here somehow")
                    return render(request, "encyclopedia/not_found.html", {
                        'form': SearchForm(),
                        'errorRequest': Q
                    })

def new_entry(request, *args, **kwargs):
    if request.method=="POST":
        data=NewEntryForm(request.POST)
        print(data)
        if data.is_valid:
            title=data.cleaned_data['title']
            content=data.cleaned_data['content']
            if util.get_entry(title) != None:
                return index(request)
            else:
                util.save_entry(title, content)
                return redirect('title', title=title)

    else:
        Q=title
        return render(request, "encyclopedia/new_entry.html", {
            "title": Q,
            "form": SearchForm(),
            "NewEntryForm": NewEntryForm()
            })

def edit_content(request, title):
    if request.method=='GET':
        data = util.get_entry(title)

        return render(request, "encyclopedia/edit.html", {
            "form": SearchForm(),
            "editForm": EditContentForm(initial={"content": data}),
            "title": title
            })
    
    else:
        data = EditContentForm(request.POST)
        if data.is_valid():
            content=data.cleaned_data["content"]
            util.save_entry(title, content)
            print("this is the title as it is", title)
            return redirect('title', title=title)

def random_page(request):
    return title(request, random.choice(util.list_entries()))

