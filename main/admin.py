from django.contrib import admin
from .models import categories, job_offers, favorites, applications, languages

# Register your models here.
admin.site.register(categories)
admin.site.register(job_offers)
admin.site.register(favorites)
admin.site.register(applications)
admin.site.register(languages)
