from django.conf import settings
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.permissions import IsAuthenticatedMongo, IsStaffUser
from .models import Booking
from accounts.models import User
from doctors.models import Doctor
from services.models import Service


def notify_clinic_of_booking(booking: Booking):
    """Email the clinic whenever a new booking is created.
    Failures here are logged but never block the booking from being saved."""
    patient = booking.patient_ref
    subject = f"New Booking — {patient.name if patient else 'Patient'}"
    body = (
        f"A new booking was made on the website.\n\n"
        f"Patient: {patient.name if patient else '-'}\n"
        f"Patient Email: {patient.email if patient else '-'}\n"
        f"Patient Phone: {patient.phone if patient else '-'}\n"
        f"Doctor: {booking.doctor_ref.name if booking.doctor_ref else '-'}\n"
        f"Service: {booking.service_ref.name if booking.service_ref else '-'}\n"
        f"Date: {booking.date}\n"
        f"Time Slot: {booking.time_slot}\n"
        f"Status: {booking.status}\n\n"
        f"Log in to the staff dashboard for details."
    )
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CLINIC_NOTIFICATION_EMAIL],
            fail_silently=True,
        )
    except Exception:
        pass


def booking_to_dict(b: Booking):
    return {
        "id": str(b.id),
        "patient_ref": str(b.patient_ref.id) if b.patient_ref else None,
        "doctor_ref": str(b.doctor_ref.id) if b.doctor_ref else None,
        "service_ref": str(b.service_ref.id) if b.service_ref else None,
        "date": b.date,
        "time_slot": b.time_slot,
        "status": b.status,
        "created_at": b.created_at.isoformat(),
    }


class BookingListCreateView(APIView):
    permission_classes = [IsAuthenticatedMongo]

    def get(self, request):
        if request.user.role == "staff":
            bookings = Booking.objects.order_by("-created_at")
        else:
            bookings = Booking.objects(patient_ref=request.user.id).order_by("-created_at")
        return Response([booking_to_dict(b) for b in bookings])

    def post(self, request):
        data = request.data
        doctor = Doctor.objects(id=data.get("doctor_ref")).first()
        service = Service.objects(id=data.get("service_ref")).first()
        if not doctor or not service:
            return Response({"error": "Valid doctor_ref and service_ref required"}, status=400)
        if not data.get("date") or not data.get("time_slot"):
            return Response({"error": "date and time_slot required"}, status=400)

        patient = User.objects(id=request.user.id).first()
        booking = Booking(
            patient_ref=patient,
            doctor_ref=doctor,
            service_ref=service,
            date=data["date"],
            time_slot=data["time_slot"],
        )
        booking.save()
        notify_clinic_of_booking(booking)
        return Response(booking_to_dict(booking), status=status.HTTP_201_CREATED)


class BookingDetailView(APIView):
    permission_classes = [IsStaffUser]

    def patch(self, request, pk):
        try:
            booking = Booking.objects.get(id=pk)
        except Booking.DoesNotExist:
            return Response({"error": "Not found"}, status=404)
        status_val = request.data.get("status")
        if status_val not in Booking.STATUS_CHOICES:
            return Response({"error": "Invalid status"}, status=400)
        booking.status = status_val
        booking.save()
        return Response(booking_to_dict(booking))
