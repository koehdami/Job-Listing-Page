from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse
from .models import user_data, categories, job_offers, languages, contactRequests, applications
from django.contrib.auth.decorators import login_required
from .forms import ContactForm
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
                "message":"There is no user with your given credentials"
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


@login_required
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

# create form and render it in get request, validate form and create entrie in db
def contact(request, message=""):
    if request.user.is_authenticated:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email':request.user.email,
        }
    else:
        initial_data = {}

    if request.method == "POST":
        # section to send error messages in post request
        if message:
            form = ContactForm(initial=initial_data)
            return render(request, "main/contact.html", {
                "form":form,
                "message":message
            })
        
        # validate form and try: to create entrie
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                contactRequests.objects.create(
                    first_name = form.cleaned_data["first_name"],
                    last_name = form.cleaned_data["last_name"],
                    email = form.cleaned_data["email"],
                    phone_number = form.cleaned_data["phone_number"],
                    content = form.cleaned_data["context"]
                )
                return contact(request, "Successfully created request, u will get a response soon.")
            except:
                return contact(request, "Error, request couldn't be created")
        else:
            return contact(request, "Form not valid, please try again.")

    else:
        form = ContactForm(initial=initial_data)

        # make the data fixed if user is logged in
        if request.user.is_authenticated:
            form.fields["first_name"].widget.attrs['disabled'] = True
            form.fields["last_name"].widget.attrs['disabled'] = True
            form.fields["email"].widget.attrs['disabled'] = True

        return render(request, "main/contact.html", {
            "form":form
        })

@login_required
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
    

@login_required
def mylistings(request):
    return render(request, "main/mylistings.html", {
        "user":request.user,
        "jobs":job_offers.objects.all()
    })

@login_required
def deletePosting(request):
    if request.method == "POST":
        if "job_id" in request.POST:
            try:
                job_listing = job_offers.objects.get(id=request.POST["job_id"])
                if job_listing.user == request.user:
                    job_listing.delete()
                    return mylistings(request)
                else:
                    return render(request, "main/mylistings.html", {
                        "user":request.user,
                        "jobs":job_offers.objects.all(),
                        "message":"You can't delete posts from other users."
                    })
            except:
                return render(request, "main/mylistings.html", {
                    "user":request.user,
                    "jobs":job_offers.objects.all(),
                    "message":"Couldn't delete posting, please try again."
                })
    else:
        return redirect("mylistings")
    
@login_required
def editPosting(request):
    if request.method == "POST":
        # if id comes from createPosting, extract values and update entrie in db
        if "job_id_edit" in request.POST:
                try:
                    category_entrie = categories.objects.get(id=request.POST["category"])
                    language_entrie = languages.objects.get(id=request.POST["language"])
                    job = job_offers.objects.get(id=request.POST["job_id_edit"])
                    if job.user == request.user:
                        job.title = request.POST["title"]
                        job.company = request.POST["companyName"]
                        job.description = request.POST["jobDescription"]
                        job.category = category_entrie
                        job.languages = language_entrie
                        job.part_time = request.POST["time"]
                        job.pay = request.POST["jobPay"]
                        job.save()
                        return redirect("mylistings")
                    else:
                        return render(request, "main/mylistings.html", {
                            "user":request.user,
                            "jobs":job_offers.objects.all(),
                            "message":"You can't edit posts from other users."
                        })
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
    

def jobPage(request, id, message=""):
    applied = False
    # get id from url and check for job in db, else render error => check if user allready applied
    try:
        jobListing = job_offers.objects.get(id=id)
        jobApplications = applications.objects.filter(job_offer_id=id)
        for application in jobApplications:
            if application.user_id == request.user:
                applied = True

        return render(request, "main/jobPage.html", {
            "job":jobListing,
            "user":request.user,
            "message":message,
            "applied":applied
        })
    except:
        return render(request, "main/index.html", {
            "message":"Error, couldn't find job. Please try agian."
        })
    
@login_required
def apply(request):
    if request.method == "POST":
        if not "job_id" in request.POST:
            return HttpResponse("Error job_id not found")
        try:
            job = job_offers.objects.get(id=request.POST["job_id"])
        except:
            return HttpResponse("Job is not listed.")
        
        # check if allready applied if yes remove else create
        if applications.objects.filter(user_id=request.user, job_offer_id=job).exists():
            activeApplications = applications.objects.get(user_id=request.user, job_offer_id=job)
            activeApplications.delete()
            return jobPage(request, request.POST["job_id"], "Successfully withdrawn application.")
        else:
            applications.objects.create(user_id=request.user, job_offer_id=job)
            return jobPage(request, request.POST["job_id"], "Successfully applied to job.")

    else:
        return redirect("/jobs")