import os
from django.shortcuts import render, redirect
import markdown2 as mk
from django import forms
from . import util
import random

class Newform(forms.Form):
    title = forms.CharField()
    text = forms.CharField(widget=forms.Textarea(attrs={"rows":'2',"cols":'2', "placeholder":"Enter text in Markdown"}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if util.get_entry(title)== None:
        return render(request, "encyclopedia/error.html")
    else:
        html = mk.markdown(util.get_entry(title))
        return render(request, "encyclopedia/entry.html",{"content":html, "title":title})

def search(request):
    title = request.GET.get("q").lower()
    if util.get_entry(title)== None:
        li=[]
        for entry in util.list_entries():
            if (title in entry.lower()):
                li.append(entry)
        if len(li)==0:
            return render(request, "encyclopedia/error.html")
        else:
            return render(request, "encyclopedia/search.html", {"lists":li})
    else:
        return redirect("entry", title=title)
    
def new(request):
    if request.method == "POST":
        form=Newform(request.POST)
        if form.is_valid():
            title=form.cleaned_data["title"]
            content=form.cleaned_data["text"]
            if util.get_entry(title)== None:
                util.save_entry(title,content)
                return render(request, "encyclopedia/entry.html",{"content":content, "title":title})
            else:
                return render(request, "encyclopedia/error.html")
            
    else:
        form=Newform()
        return render(request, "encyclopedia/new.html", {"form":form})

def edit(request, title):
    if request.method=="POST":
        content = request.POST.get("content")
        util.save_entry(title,content)
        return redirect("entry", title=title)
    content = util.get_entry(title)

    return render(request, "encyclopedia/edit.html", {'title':title, 'content': content})

def rand(request):
    l = len(util.list_entries())
    print(l)
    r = random.randint(0,l)
    title = util.list_entries()
    title=title[r]
    return redirect('entry', title=title)