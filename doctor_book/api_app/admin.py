from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register((Tbl_Doctor,Tbl_Patient,Tbl_Appointment))
