import datetime as dt
from mongoengine import (
    Document, StringField, EmailField, ReferenceField, DateTimeField, NULLIFY
)
from doctors.models import Doctor
from services.models import Service


class AppointmentEnquiry(Document):
    STATUS_CHOICES = ("new", "contacted", "converted")

    name = StringField(required=True, max_length=120)
    phone = StringField(required=True, max_length=20)
    email = EmailField(required=True)
    service_ref = ReferenceField(Service, reverse_delete_rule=NULLIFY)
    doctor_ref = ReferenceField(Doctor, reverse_delete_rule=NULLIFY, required=False)
    preferred_date = StringField(required=True)  # ISO date string, kept simple for MVP
    message = StringField(default="")
    status = StringField(choices=STATUS_CHOICES, default="new")
    created_at = DateTimeField(default=dt.datetime.utcnow)

    meta = {"collection": "appointment_enquiries", "ordering": ["-created_at"]}
