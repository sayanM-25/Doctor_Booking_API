from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework import status
from datetime import datetime, timedelta
from django.utils.dateparse import parse_date
from .custompermissions import My_permission,Patient_permission
from django.core.mail import send_mail
from rest_framework.authentication import TokenAuthentication


# Create your views here.

class LoginAPIView(APIView):
    authentication_classes=[TokenAuthentication]
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        
        if not serializer.is_valid():
            context = {
                "status_code": 400,
                "message": "Invalid data provided.",
                "data": serializer.errors
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user_obj = authenticate(username=username, password=password)
        if user_obj is not None:
            token, created = Token.objects.get_or_create(user=user_obj)
            response_data = {
                "token": str(token)
            }
            context = {
                "status_code": 200,
                "message": "Login successful.",
                "data": response_data
            }
            return Response(context, status=status.HTTP_200_OK)
        
        context = {
            "status_code": 400,
            "message": "Invalid credentials.",
            "data": {}
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

class RegistrationAPIView(APIView):

    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)  
        if serializer.is_valid():
            user = serializer.save()  
            token, created = Token.objects.get_or_create(user=user)  
            
            response_data = {
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'token': token.key
            }
            context = {
                'status_code': 200,
                'message': 'User registered successfully.',
                'data': response_data
            }
            return Response(context, status=status.HTTP_201_CREATED)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes=[My_permission]
      
    def get(self, request, id=None):
        if id:
            try:
                doctor = Tbl_Doctor.objects.get(pk=id)
                serializer = Tbl_DoctorSerializer(doctor)
                context = {
                    "status_code": 200,
                    "message": "Doctor retrieved successfully.",
                    "data": serializer.data
                }
                return Response(context, status=status.HTTP_200_OK)
            except Tbl_Doctor.DoesNotExist:
                context = {
                    "status_code": 404,
                    "message": "Doctor not found.",
                    "data": {}
                }
                return Response(context, status=status.HTTP_404_NOT_FOUND)
        else:
            doctors = Tbl_Doctor.objects.all().order_by('-pk')
            serializer = Tbl_DoctorSerializer(doctors, many=True)
            context = {
                "status_code": 200,
                "message": "Doctors retrieved successfully.",
                "data": serializer.data
            }
            return Response(context, status=status.HTTP_200_OK)

    
    def post(self, request):
       
        data = request.data
        serializer = Tbl_DoctorSerializer(data=data)
        if not serializer.is_valid():
            context = {
                'status_code': 400,
                'message': 'Invalid data provided',
                'data': serializer.errors
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        context = {
            'status_code': 201,
            'message': 'Doctor created successfully',
            'data': serializer.data
        }
        return Response(context, status=status.HTTP_201_CREATED)

    def put(self, request, id):
        try:
            doctor = Tbl_Doctor.objects.get(pk=id)
        except Tbl_Doctor.DoesNotExist:
            context = {
                'status_code': 404,
                'message': 'Doctor not found',
                'data': {}
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        
        serializer = Tbl_DoctorSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = {
                'status_code': 200,
                'message': 'Doctor updated successfully',
                'data': serializer.data
            }
            return Response(context, status=status.HTTP_200_OK)
        
        context = {
            'status_code': 400,
            'message': 'Invalid data provided',
            'data': serializer.errors
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, id):
        try:
            doctor = Tbl_Doctor.objects.get(pk=id)
        except Tbl_Doctor.DoesNotExist:
            context = {
                'status_code': 404,
                'message': 'Doctor not found',
                'data': {}
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        
        doctor.delete()
        context = {
            'status_code': 204,
            'message': 'Doctor deleted successfully',
            'data': {}
        }
        return Response(context, status=status.HTTP_204_NO_CONTENT)

class PatientAPIView(APIView):
    # permission_classes = [IsAuthenticated] 
    permission_classes=[Patient_permission]
    def get(self, request, id=None):
        if id:
            try:
                patient = Tbl_Patient.objects.get(pk=id)
                serializer = Tbl_PatientSerializer(patient)
                context = {
                    "status_code": 200,
                    "message": "Patient retrieved successfully.",
                    "data": serializer.data
                }
                return Response(context, status=status.HTTP_200_OK)
            except Tbl_Patient.DoesNotExist:
                context = {
                    "status_code": 404,
                    "message": "Patient not found.",
                    "data": {}
                }
                return Response(context, status=status.HTTP_404_NOT_FOUND)
        else:
            patients = Tbl_Patient.objects.all().order_by('-pk')
            serializer = Tbl_PatientSerializer(patients, many=True)
            context = {
                "status_code": 200,
                "message": "Patients retrieved successfully.",
                "data": serializer.data
            }
            return Response(context, status=status.HTTP_200_OK)


    def put(self, request, id):
        try:
            patient = Tbl_Patient.objects.get(pk=id)
        except Tbl_Patient.DoesNotExist:
            context = {
                'status_code': 404,
                'message': 'Patient not found',
                'data': {}
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        
        serializer = Tbl_PatientSerializer(patient, data=request.data)
        if not serializer.is_valid():
            context = {
                'status_code': 400,
                'message': 'Invalid data provided',
                'data': serializer.errors
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        context = {
            'status_code': 200,
            'message': 'Patient updated successfully',
            'data': serializer.data
        }
        return Response(context, status=status.HTTP_200_OK)

    
    def delete(self, request, id):
        try:
            patient = Tbl_Patient.objects.get(pk=id)
        except Tbl_Patient.DoesNotExist:
            context = {
                'status_code': 404,
                'message': 'Patient not found',
                'data': {}
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        
        patient.delete()
        context = {
            'status_code': 204,
            'message': 'Patient deleted successfully',
            'data': {}
        }
        return Response(context, status=status.HTTP_204_NO_CONTENT)

class ApointmentAPIView(APIView):

    def get(self, request, id=None):
        if id:
            try:
                appointment = Tbl_Appointment.objects.get(pk=id)
                serializer = Tbl_AppointmentSerializer(appointment)
                context = {
                    "status_code": 200,
                    "message": "Appointment retrieved successfully.",
                    "data": serializer.data
                }
                return Response(context, status=status.HTTP_200_OK)
            except Tbl_Appointment.DoesNotExist:
                context = {
                    "status_code": 404,
                    "message": "Appointment not found.",
                    "data": {}
                }
                return Response(context, status=status.HTTP_404_NOT_FOUND)
        else:
            appointment = Tbl_Appointment.objects.all().order_by('-pk')
            serializer = Tbl_AppointmentSerializer(appointment, many=True)
            context = {
                "status_code": 200,
                "message": "Appointment retrieved successfully.",
                "data": serializer.data
            }
            return Response(context, status=status.HTTP_200_OK)
        
    def put(self, request, id):
        try:
            appointment = Tbl_Appointment.objects.get(pk=id)
        except Tbl_Appointment.DoesNotExist:
            context = {
                'status_code': 404,
                'message': 'Appointment not found',
                'data': {}
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        
        serializer = Tbl_AppointmentSerializer(appointment, data=request.data)
        if not serializer.is_valid():
            context = {
                'status_code': 400,
                'message': 'Invalid data provided',
                'data': serializer.errors
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        context = {
            'status_code': 200,
            'message': 'Appointment updated successfully',
            'data': serializer.data
        }
        return Response(context, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        try:
            appointment = Tbl_Appointment.objects.get(pk=id)
        except Tbl_Appointment.DoesNotExist:
            context = {
                'status_code': 404,
                'message': 'Appointment not found',
                'data': {}
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        
         # Send email notifications
        patient_email = appointment.patient.Fld_email
        doctor_email = appointment.doctor.Fld_contact_number  # Assuming this is the email field
        patient_name = appointment.patient.Fld_name
        doctor_name = appointment.doctor.Fld_name
        appointment_date = appointment.Fld_appointment_date
        slot = appointment.Fld_slot
        
        #Cancellation notification to patient

        send_mail(
            "Appointment Cancellation",
            f"""
            Dear {patient_name},

            Your appointment with Dr. {doctor_name} on {appointment_date} at {slot} has been cancelled.

            We apologize for any inconvenience caused.

            Best regards,
            Anonymous Clinic Team
            """,
            'isayan635@gmail.com',
            [patient_email],
            fail_silently=False,
        )

        #Cancellation notification to doctor

        send_mail(
            "Appointment Cancellation",
            f"""
            Dear Dr. {doctor_name},

            The appointment with patient {patient_name} on {appointment_date} at {slot} has been cancelled.

            We apologize for any inconvenience caused.

            Best regards,
            Anonymous Clinic Team
            """,
            'isayan635@gmail.com',
            [doctor_email],
            fail_silently=False,
        )
        
        appointment.delete()
        context = {
            'status_code': 204,
            'message': 'Appointment deleted successfully',
            'data': {}
        }
        return Response(context, status=status.HTTP_204_NO_CONTENT)


class AvailableSlotsView(APIView):
    def get(self, request, doctor_id):
        try:
            doctor = Tbl_Doctor.objects.get(pk=doctor_id)
        except Tbl_Doctor.DoesNotExist:
            return Response(
                {"status_code": 404, 
                 "message": "Doctor not found", 
                 "data": {}}, status=status.HTTP_404_NOT_FOUND)
        
        current_date = datetime.now().date()
        week_end_date = current_date + timedelta(days=7)
        
        booked_slots = Tbl_Appointment.objects.filter(
            doctor=doctor,
            Fld_appointment_date__range=(current_date, week_end_date)
        ).values_list('Fld_slot', flat=True)
        
        available_slots = [
            {"day": day, "slots": [slot for slot in slots if slot not in booked_slots]}
            for day, slots in doctor.Fld_available_slots.items()
        ]
        
        data = {"available_slots": available_slots}
        serializer = AvailableSlotSerializer(data=data)
        
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class BookAppointmentView(APIView):
    def post(self, request):
        serializer = Tbl_AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            doctor_id = request.data.get('doctor')
            slot = request.data.get('Fld_slot')
            appointment_date = parse_date(request.data.get('Fld_appointment_date'))
            
            try:
                doctor = Tbl_Doctor.objects.get(pk=doctor_id)
            except Tbl_Doctor.DoesNotExist:
                return Response(
                    {"status_code": 404, 
                     "message": "Doctor not found", 
                     "data": {}}, status=status.HTTP_404_NOT_FOUND)
            
            current_date = datetime.now().date()
            week_end_date = current_date + timedelta(days=7)
            
            booked_slots = Tbl_Appointment.objects.filter(
                doctor=doctor,
                Fld_appointment_date__range=(current_date, week_end_date)
            ).values_list('Fld_slot', flat=True)
            
            if slot in booked_slots:
                available_slots = [
                    {"day": day, "slots": [slot for slot in slots if slot not in booked_slots]}
                    for day, slots in doctor.Fld_available_slots.items()
                ]
                
                data = {"available_slots": available_slots}
                available_slots_serializer = AvailableSlotSerializer(data=data)
                
                if available_slots_serializer.is_valid():
                    return Response({
                        "status_code": 400,
                        "message": "Slot already booked",
                        "available_slots": available_slots_serializer.data["available_slots"]
                    }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(available_slots_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            appointment = serializer.save()
            
            patient_email = appointment.patient.Fld_email
            doctor_email = doctor.Fld_email
            patient_name = appointment.patient.Fld_name
            doctor_name = doctor.Fld_name
            appointment_date = appointment.Fld_appointment_date


            #Booking confirmation to patient

            send_mail(
                "Appointment Confirmation",
                f"""
                Dear {patient_name},

                Your appointment with Dr. {doctor_name} has been confirmed.

                Date: {appointment_date}
                Time: {slot}

                Thank you for choosing our services.

                Best regards,
                Anonymous Clinic Team
                """,
                'isayan635@gmail.com',
                [patient_email],
                fail_silently=False,
            )
            
            #Booking confirmation to doctor

            send_mail(
                "Appointment Confirmation",
                f"""
                Dear Dr. {doctor_name},

                An appointment has been booked with patient {patient_name}.

                Date: {appointment_date}
                Time: {slot}

                Best regards,
                Anonymous Clinic Team
                """,
                'isayan635@gmail.com',
                [doctor_email],
                fail_silently=False,
            )

            return Response({"status_code": 201,
                            "message": "Appointment booked successfully",
                            "data": serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response({"status_code": 400,
                          "message": "Invalid data provided", 
                          "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get the user's token
        user = request.user
        try:
            token = Token.objects.get(user=user)
            token.delete()  # Delete the token
            context = {
                "status_code": 200,
                "message": "Logout successful."
            }
            return Response(context, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            context = {
                "status_code": 400,
                "message": "Token not found."
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
