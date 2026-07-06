import datetime as dt
from mongoengine import Document, StringField, ReferenceField, DateTimeField, NULLIFY
from accounts.models import User
from doctors.models import Doctor
from services.models import Service


class Booking(Document):
    STATUS_CHOICES = ("pending", "confirmed", "completed", "cancelled")

    patient_ref = ReferenceField(User, reverse_delete_rule=NULLIFY)
    doctor_ref = ReferenceField(Doctor, reverse_delete_rule=NULLIFY)
    service_ref = ReferenceField(Service, reverse_delete_rule=NULLIFY)
    date = StringField(required=True)
    time_slot = StringField(required=True)
    status = StringField(choices=STATUS_CHOICES, default="pending")
    created_at = DateTimeField(default=dt.datetime.utcnow)

    meta = {"collection": "bookings", "ordering": ["-created_at"]}
