from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class user_data(models.Model):
    name = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    current_job = models.CharField(max_length=64, default="")
    job_title = models.CharField(max_length=64, default="")
    phone_number = models.CharField(max_length=32, default="")

    def __str__(self):
        return f"{self.name} is working at {self.current_job} as a {self.job_title} Phonenumber:{self.phone_number}"

class categories(models.Model):
    id = models.IntegerField(primary_key=True, unique=True),
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"Name:{self.name}, Id:{self.id}"

class languages(models.Model):
    id = models.IntegerField(primary_key=True, unique=True),
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"Name:{self.name}, Id:{self.id}"


class job_offers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    id = models.IntegerField(primary_key=True, unique=True),
    category = models.ForeignKey(categories, on_delete=models.CASCADE)
    pay = models.CharField(max_length=64)
    languages = models.ForeignKey(languages, on_delete=models.CASCADE)
    company = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    post_date = models.DateTimeField(auto_now=True)
    part_time = models.BooleanField(default=False)

    def __str__(self):
        return f"Job {self.id} with title {self.title} from {self.user}"

class applications(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    job_offer_id = models.ForeignKey(job_offers, on_delete=models.CASCADE)

    def __str__(self):
        return f"Id:{self.id} User {self.user_id} applied to {self.job_offer_id}"
    
    def valid_user(self):
        return self.user_id != self.job_offer_id.user
    
class contactRequests(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    first_name = models.TextField(max_length=64)
    last_name = models.TextField(max_length=64)
    email = models.EmailField()
    phone_number = models.TextField(max_length=32)
    content = models.CharField(max_length=512)

    def __str__(self):
        return f"{self.first_name}  {self.last_name}, requestedID: {self.id}"
    
    def valid_request(self):
        return self.first_name != self.last_name