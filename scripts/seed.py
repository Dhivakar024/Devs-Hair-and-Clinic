"""
Seed script — run with: python scripts/seed.py
Populates sample doctors, services, a staff user, and a couple enquiries.
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clinic_backend.settings")
django.setup()

from accounts.models import User
from doctors.models import Doctor, AvailabilitySlot
from services.models import Service
from enquiries.models import AppointmentEnquiry


def seed():
    if not User.objects(email="admin@devsclinic.com").first():
        staff = User(email="admin@devsclinic.com", name="Clinic Admin", role="staff", phone="9999999999")
        staff.set_password("Admin@123")
        staff.save()
        print("Created staff user: admin@devsclinic.com / Admin@123")

    if Doctor.objects.count() == 0:
        Doctor(
            name="Dr. Ananya Rao",
            photo_url="https://images.unsplash.com/photo-1651008376811-b90baee60c1f?w=800&q=80&auto=format&fit=crop",
            specialties=["Dermatology", "Trichology", "Cosmetic Skin Care"],
            qualifications="MBBS, MD Dermatology, Fellowship in Aesthetic Medicine",
            bio=(
                "Dr. Ananya Rao has spent over 12 years helping patients feel confident in "
                "their skin and hair. She combines modern dermatological science with a warm, "
                "unhurried consultation style — because good care starts with really listening."
            ),
            availability=[
                AvailabilitySlot(day="Monday", start_time="10:00", end_time="16:00"),
                AvailabilitySlot(day="Wednesday", start_time="10:00", end_time="16:00"),
                AvailabilitySlot(day="Friday", start_time="11:00", end_time="18:00"),
                AvailabilitySlot(day="Saturday", start_time="09:00", end_time="13:00"),
            ],
        ).save()
        print("Seeded 1 doctor")

    if Service.objects.count() == 0:
        Service(
            name="Acne & Scar Consultation", category="Skin",
            description="Diagnosis and a personalized treatment plan for acne and scarring.",
            price=800, duration_mins=30,
            image_url="https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=600&q=80&auto=format&fit=crop",
        ).save()
        Service(
            name="Hair Fall & Scalp Therapy", category="Hair",
            description="Complete assessment and therapy plan to restore hair and scalp health.",
            price=1200, duration_mins=45,
            image_url="https://images.unsplash.com/photo-1519415943484-9fa1873496d4?w=600&q=80&auto=format&fit=crop",
        ).save()
        Service(
            name="Chemical Peel", category="Skin",
            description="Skin rejuvenation peel treatment for a brighter, smoother complexion.",
            price=2500, duration_mins=60,
            image_url="https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=600&q=80&auto=format&fit=crop",
        ).save()
        Service(
            name="Laser Hair Removal", category="Skin",
            description="Painless, precise laser hair reduction for smooth, lasting results.",
            price=3000, duration_mins=45,
            image_url="https://images.unsplash.com/photo-1600334129128-685c5582fd35?w=600&q=80&auto=format&fit=crop",
        ).save()
        Service(
            name="Hair Transplant Consultation", category="Hair",
            description="Expert evaluation for hair transplant candidacy and planning.",
            price=1000, duration_mins=30,
            image_url="https://images.unsplash.com/photo-1580281657702-257584239a55?w=600&q=80&auto=format&fit=crop",
        ).save()
        print("Seeded 5 services")

    if AppointmentEnquiry.objects.count() == 0:
        svc = Service.objects.first()
        AppointmentEnquiry(name="Priya S", phone="9876543210", email="priya@example.com", service_ref=svc, preferred_date="2026-07-10", message="Interested in acne consult").save()
        AppointmentEnquiry(name="Rahul K", phone="9123456780", email="rahul@example.com", service_ref=svc, preferred_date="2026-07-12", message="Hair fall concern").save()
        print("Seeded 2 sample enquiries")

    print("Seeding complete.")


if __name__ == "__main__":
    seed()
