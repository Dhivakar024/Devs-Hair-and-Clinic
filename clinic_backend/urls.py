from django.urls import path, include

urlpatterns = [
    path("api/auth/", include("accounts.urls")),
    path("api/doctors/", include("doctors.urls")),
    path("api/services/", include("services.urls")),
    path("api/enquiries/", include("enquiries.urls")),
    path("api/bookings/", include("bookings.urls")),
]
