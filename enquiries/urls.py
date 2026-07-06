from django.urls import path
from .views import EnquiryListCreateView, EnquiryDetailView

urlpatterns = [
    path("", EnquiryListCreateView.as_view(), name="enquiry-list"),
    path("<str:pk>/", EnquiryDetailView.as_view(), name="enquiry-detail"),
]
