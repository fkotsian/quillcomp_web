from django.contrib import admin
from .models import Prompt, StudentResponse

# Register your models here.
admin.site.register(Prompt)
admin.site.register(StudentResponse)
