from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from .models import user_data, categories, job_offers, languages
import json

# Create your views here.


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, "main/index.html", {
                "message":"Sucessfully logged in.",
                "user":request.user
            })
    else:
        return render(request, "main/login.html", {
            "user":request.user
        })

def logout_user(request):
    logout(request)
    return render(request, "main/index.html", {
        "user":request.user
    })

def register_user(request):
    if request.method == "POST":
        if "password" in request.POST and "password-check" in request.POST:
            password = request.POST["password"]
            passwordCheck = request.POST["password-check"]
            if password == passwordCheck:
                try:
                    user = User.objects.create_user(
                        username=request.POST["username"], 
                        email=request.POST["email"], 
                        password=password, 
                        first_name=request.POST["firstname"], 
                        last_name=request.POST["lastname"])
                    return render(request, "main/index.html", {
                        "message":"Account created.",
                        "user":True
                    })
                except:
                    return render(request, "main/register.html", {
                        "message":"Something went wrong, try again or contact support."
                    })
            else:
                return render(request, "main/register.html", {
                "message":"Passwords don't match, please try again!"
            })
        else:
            return render(request, "main/register.html", {
                "message":"Passwords not provided, try again!"
            })

    return render(request, "main/register.html", {
        "user":request.user
    })

def index(request):
    return render(request, "main/index.html", {
        "user":request.user
    })



def profile(request):
    if request.method == "POST":
        try:
            userData = user_data.objects.get(name=request.user)
        except:
            userData = user_data.objects.create(name=request.user)
        if "current-job" in request.POST:
            userData.current_job = request.POST["current-job"]
        if "title-job" in request.POST:
            userData.job_title = request.POST["title-job"]
        userData.save()
        
        return render(request, "main/profile.html", {
            "user":request.user,
            "message":"User updated."
        })

    if not request.user.is_authenticated:
        return render(request, "main/login.html", {
            "user":request.user
        })
    return render(request, "main/profile.html", {
        "user":request.user
    })

def jobs(request):
    return render(request, "main/jobs.html", {
        "user":request.user,
        "categories":categories.objects.all(),
        "languages":languages.objects.all(),
        "jobs":job_offers.objects.all()
    })

def contact(request):
    return render(request, "main/contact.html", {
        "user":request.user
    })

def createListing(request):
    if request.method == "POST":
        try:
            job_offers.objects.create(
                user = request.user,
                title = request.POST["title"],
                company = request.POST["companyName"],
                description = request.POST["jobDescription"],
                pay = request.POST["jobPay"],
                category = categories.objects.get(id=request.POST["language"]),
                languages = languages.objects.get(id=request.POST["category"]),
                part_time = request.POST["time"],
            )
            return redirect("/jobs")
        except:
            return render(request, "main/createListing.html", {
                "message":"Listing creation didn't work, please try again.",
                "user":request.user,
                "categories":categories.objects.all(),
                "languages":languages.objects.all()
            })

    else:
        return render(request, "main/createListing.html", {
            "user":request.user,
            "categories":categories.objects.all(),
            "languages":languages.objects.all()
        })
    

def mylistings(request):
    return render(request, "main/mylistings.html", {
        "user":request.user,
        "jobs":job_offers.objects.all()
    })

def deletePosting(request):
    if request.method == "POST":
        if "job_id" in request.POST:
            try:
                job_listing = job_offers.objects.get(id=request.POST["job_id"])
                job_listing.delete()
                return mylistings(request)
            except:
                return render(request, "main/mylistings.html", {
                    "user":request.user,
                    "jobs":job_offers.objects.all(),
                    "message":"Couldn't delete posting, please try again."
                })
    else:
        return redirect("mylistings")
    

def editPosting(request):
    if request.method == "POST":
        # if id comes from createPosting, extract values and update entrie in db
        if "job_id_edit" in request.POST:
                try:
                    category_entrie = categories.objects.get(id=request.POST["category"])
                    language_entrie = languages.objects.get(id=request.POST["language"])
                    job = job_offers.objects.get(id=request.POST["job_id_edit"])
                    job.title = request.POST["title"]
                    job.company = request.POST["companyName"]
                    job.description = request.POST["jobDescription"]
                    job.category = category_entrie
                    job.languages = language_entrie
                    job.part_time = request.POST["time"]
                    job.pay = request.POST["jobPay"]
                    job.save()
                    return redirect("mylistings")
                except:
                    return render(request, "main/mylistings.html", {
                        "user":request.user,
                        "jobs":job_offers.objects.all(),
                        "message":"Error while editing post, please try again."
                    })

        else:
            # get id from myPosting then try to render createListing mit edit true so the submit btn changes    
            try:
                job = job_offers.objects.get(id=request.POST["job_id"])
            except:
                return render(request, "main/mylistings.html", {
                    "user":request.user,
                    "jobs":job_offers.objects.all(),
                    "message":"Couldn't edit posting, please try again."
                })
                
            return render(request, "main/createListing.html", {
                "user":request.user,
                "categories":categories.objects.all(),
                "languages":languages.objects.all(),
                "job":job,
                "edit":True
            })
    else:
        return redirect("mylistings")