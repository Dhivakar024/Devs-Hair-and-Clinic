import re
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.permissions import IsStaffUser
from .models import AppointmentEnquiry
from doctors.models import Doctor
from services.models import Service

PHONE_RE = re.compile(r"^\+?[0-9]{10,15}$")


def notify_clinic_of_enquiry(enquiry: AppointmentEnquiry):
    """Email the clinic whenever a new appointment enquiry comes in.
    Failures here are logged but never block the enquiry from being saved."""
    subject = f"New Appointment Enquiry — {enquiry.name}"
    body = (
        f"A new appointment enquiry was submitted on the website.\n\n"
        f"Name: {enquiry.name}\n"
        f"Phone: {enquiry.phone}\n"
        f"Email: {enquiry.email}\n"
        f"Service: {enquiry.service_ref.name if enquiry.service_ref else '-'}\n"
        f"Preferred Date: {enquiry.preferred_date}\n"
        f"Message: {enquiry.message or '-'}\n\n"
        f"Log in to the staff dashboard to follow up."
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


def enquiry_to_dict(e: AppointmentEnquiry):
    return {
        "id": str(e.id),
        "name": e.name,
        "phone": e.phone,
        "email": e.email,
        "service_ref": str(e.service_ref.id) if e.service_ref else None,
        "doctor_ref": str(e.doctor_ref.id) if e.doctor_ref else None,
        "preferred_date": e.preferred_date,
        "message": e.message,
        "status": e.status,
        "created_at": e.created_at.isoformat(),
    }


class EnquiryListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [IsStaffUser()]
        return []  # public can submit enquiries

    def get(self, request):
        enquiries = AppointmentEnquiry.objects.order_by("-created_at")
        return Response([enquiry_to_dict(e) for e in enquiries])

    def post(self, request):
        data = request.data
        errors = {}
        if not data.get("name"):
            errors["name"] = "Name is required"
        if not data.get("email"):
            errors["email"] = "Email is required"
        phone = data.get("phone", "")
        if not phone or not PHONE_RE.match(phone):
            errors["phone"] = "Valid phone number is required (10-15 digits)"
        if not data.get("preferred_date"):
            errors["preferred_date"] = "Preferred date is required"
        if not data.get("service_ref"):
            errors["service_ref"] = "Please select a service"

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        service = Service.objects(id=data["service_ref"]).first()
        if not service:
            return Response({"errors": {"service_ref": "Invalid service"}}, status=400)

        doctor = None
        if data.get("doctor_ref"):
            doctor = Doctor.objects(id=data["doctor_ref"]).first()

        enquiry = AppointmentEnquiry(
            name=data["name"],
            phone=phone,
            email=data["email"],
            service_ref=service,
            doctor_ref=doctor,
            preferred_date=data["preferred_date"],
            message=data.get("message", ""),
        )
        enquiry.save()
        notify_clinic_of_enquiry(enquiry)
        return Response(enquiry_to_dict(enquiry), status=status.HTTP_201_CREATED)


class EnquiryDetailView(APIView):
    permission_classes = [IsStaffUser]

    def patch(self, request, pk):
        try:
            enquiry = AppointmentEnquiry.objects.get(id=pk)
        except AppointmentEnquiry.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        status_val = request.data.get("status")
        if status_val not in AppointmentEnquiry.STATUS_CHOICES:
            return Response({"error": "Invalid status"}, status=400)

        enquiry.status = status_val
        enquiry.save()
        return Response(enquiry_to_dict(enquiry))
