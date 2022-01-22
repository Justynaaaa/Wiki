from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("newpage/",views.create, name="create"),
    path("edit/", views.edit, name="edit"),
    path("save/", views.save, name="save"),
    path("rndPage/", views.rndPage, name="random")
    
    

]
