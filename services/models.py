from mongoengine import Document, StringField, DecimalField, IntField, BooleanField


class Service(Document):
    name = StringField(required=True, max_length=150)
    category = StringField(default="")
    description = StringField(default="")
    price = DecimalField(required=True, precision=2)
    duration_mins = IntField(default=30)
    image_url = StringField(default="")
    active = BooleanField(default=True)

    meta = {"collection": "services"}
