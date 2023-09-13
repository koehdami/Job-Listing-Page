from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile", views.profile, name="profile"),
    path("jobs", views.jobs, name="jobs"),
    path("contact", views.contact, name="contact"),
    path('login', views.login_user, name="login"),
    path('logout', views.logout_user, name="logout"),
    path("register", views.register_user, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("mylistings", views.mylistings, name="mylistings"),
    path("deletePosting", views.deletePosting, name="deletePosting"),
    path("editPosting", views.editPosting, name="editPosting"),
    path("jobs/<str:id>", views.jobPage, name="jobPage"),
    path("apply", views.apply, name="apply")
]