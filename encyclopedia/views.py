from django.shortcuts import render
from django import forms
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown
from random import choice


class NewForm(forms.Form):
    title = forms.CharField(label = "Entry title")
    text = forms.CharField(label="Text", widget= forms.Textarea(attrs={'class' : 'form-control col-md-7 ', 'rows' :10}))
    
def index(request):
    if request.method == 'POST':
        search = request.POST('q')
    else:    
      return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    
    })

def entry(request, entry):
    md = Markdown()
    page = util.get_entry(entry)

    

    if page is None:
        return render (request,"encyclopedia/errorTitle.html", {
           "entryTitle":entry 
        })
    else:
        return render(request, "encyclopedia/title.html",
        {
         "entry": md.convert(page),
         "entryTitle": entry
         
        })



def search(request): 
    
  value = request.GET.get('q','')
  if(util.get_entry(value) is not None ):
   return HttpResponseRedirect(reverse("entry", kwargs={'entry': value}))
  
  else:
        display = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
               display.append(entry)


        return render(request, "encyclopedia/index.html", {
        "entries": display,
        "search": True,
        "value": value
        })


def create(request):
     if request.method == "POST":
        form = NewForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            if(util.get_entry(title)):
                message = "Sorry, this title already exists"
                return render(request,"encyclopedia/create.html",{
                    "form":form,
                    "message":message
                    
               })
            else:
                util.save_entry(title,text)
                return entry(request,title)

                    

        else:
            return render(request,"encyclopedia/create.html",{
                "form":form
                
            })

     return render(request, "encyclopedia/create.html",{
        "form": NewForm()
    }) 

def edit(request):
  if request.method == "POST":
      title = request.POST["title"]
     
      text = util.get_entry(title)
      return render(request,"encyclopedia/save.html",{ 
          "entry": text,
          "entryTitle": title


      })
      
def save(request):
     if request.method == "POST":

       entryTitle = request.POST["title"]
       entry = request.POST["text"]
       util.save_entry(entryTitle,entry )
       
       return render (request, "encyclopedia/index.html",{
          "entries": util.list_entries(),   
           "entryTitle": entryTitle,
          
            })

     
def rndPage(request):

   
    return entry(request,choice( util.list_entries()))
    
