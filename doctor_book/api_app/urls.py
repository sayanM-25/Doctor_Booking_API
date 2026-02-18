from django.urls import path
from .views import *
urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/',RegistrationAPIView.as_view(),name='register'),

    path('doctors/',DoctorAPIView.as_view(),name='doctors'),
    path('doctors/<int:id>/', DoctorAPIView.as_view()),

    path('patients/',PatientAPIView.as_view(),name='patients'),
    path('patients/<int:id>/',PatientAPIView.as_view()),

    path('appointments/',ApointmentAPIView.as_view(),name='appointments'),
    path('appointments/<int:id>/',ApointmentAPIView.as_view()),

    path('appointments/available-slots/<int:doctor_id>/', AvailableSlotsView.as_view(), name='available-slots'),
    path('appointments/book/', BookAppointmentView.as_view(), name='book-appointment'),
    
]