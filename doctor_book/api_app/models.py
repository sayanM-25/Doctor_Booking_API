from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tbl_Doctor(models.Model):
    Fld_name = models.CharField(max_length=255)
    Fld_specialization = models.CharField(max_length=255)
    Fld_contact_number = models.CharField(max_length=20)
    Fld_available_slots = models.JSONField()
    Fld_email = models.EmailField(null=True,blank=True)


    def __str__(self):
        return self.Fld_name

class Tbl_Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Fld_name = models.CharField(max_length=255)
    Fld_contact_number = models.CharField(max_length=20)
    Fld_email = models.EmailField()

    def __str__(self):
        return self.Fld_name
    
class Tbl_Appointment(models.Model):
    doctor = models.ForeignKey(Tbl_Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Tbl_Patient, on_delete=models.CASCADE)
    Fld_appointment_date = models.DateTimeField()
    Fld_status = models.CharField(max_length=50)
    Fld_slot = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.doctor.Fld_name} - {self.patient.Fld_name} - {self.Fld_appointment_date}'