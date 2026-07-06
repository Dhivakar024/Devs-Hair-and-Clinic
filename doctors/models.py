from mongoengine import (
    Document, EmbeddedDocument, StringField, ListField,
    EmbeddedDocumentField, BooleanField
)


class AvailabilitySlot(EmbeddedDocument):
    day = StringField(required=True)  # e.g. "Monday"
    start_time = StringField(required=True)  # "09:00"
    end_time = StringField(required=True)    # "17:00"


class Doctor(Document):
    name = StringField(required=True, max_length=120)
    photo_url = StringField(default="")
    specialties = ListField(StringField(), default=list)
    qualifications = StringField(default="")
    bio = StringField(default="")
    availability = ListField(EmbeddedDocumentField(AvailabilitySlot), default=list)
    active = BooleanField(default=True)

    meta = {"collection": "doctors"}
