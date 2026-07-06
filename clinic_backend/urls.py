from django.http import JsonResponse
from django.urls import path, include

def home(request):
    return JsonResponse({
        "message": "Devs Hair & Clinic Backend is running 🚀"
    })

urlpatterns = [
    path("", home),

    path("api/auth/", include("accounts.urls")),
    path("api/doctors/", include("doctors.urls")),
    path("api/services/", include("services.urls")),
    path("api/enquiries/", include("enquiries.urls")),
    path("api/bookings/", include("bookings.urls")),
]