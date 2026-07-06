from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.permissions import IsStaffUser
from .models import Doctor, AvailabilitySlot


def doctor_to_dict(d: Doctor):
    return {
        "id": str(d.id),
        "name": d.name,
        "photo_url": d.photo_url,
        "specialties": d.specialties,
        "qualifications": d.qualifications,
        "bio": d.bio,
        "availability": [
            {"day": a.day, "start_time": a.start_time, "end_time": a.end_time}
            for a in d.availability
        ],
        "active": d.active,
    }


class DoctorListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsStaffUser()]
        return []

    def get(self, request):
        doctors = Doctor.objects(active=True)
        return Response([doctor_to_dict(d) for d in doctors])

    def post(self, request):
        data = request.data
        if not data.get("name"):
            return Response({"error": "name is required"}, status=400)

        availability = [
            AvailabilitySlot(**slot) for slot in data.get("availability", [])
        ]
        doctor = Doctor(
            name=data["name"],
            photo_url=data.get("photo_url", ""),
            specialties=data.get("specialties", []),
            qualifications=data.get("qualifications", ""),
            bio=data.get("bio", ""),
            availability=availability,
        )
        doctor.save()
        return Response(doctor_to_dict(doctor), status=status.HTTP_201_CREATED)


class DoctorDetailView(APIView):
    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            return [IsStaffUser()]
        return []

    def get_object(self, pk):
        try:
            return Doctor.objects.get(id=pk)
        except Doctor.DoesNotExist:
            return None

    def get(self, request, pk):
        doctor = self.get_object(pk)
        if not doctor:
            return Response({"error": "Not found"}, status=404)
        return Response(doctor_to_dict(doctor))

    def put(self, request, pk):
        doctor = self.get_object(pk)
        if not doctor:
            return Response({"error": "Not found"}, status=404)
        data = request.data
        for field in ["name", "photo_url", "qualifications", "bio", "active"]:
            if field in data:
                setattr(doctor, field, data[field])
        if "specialties" in data:
            doctor.specialties = data["specialties"]
        if "availability" in data:
            doctor.availability = [AvailabilitySlot(**s) for s in data["availability"]]
        doctor.save()
        return Response(doctor_to_dict(doctor))

    def delete(self, request, pk):
        doctor = self.get_object(pk)
        if not doctor:
            return Response({"error": "Not found"}, status=404)
        doctor.active = False
        doctor.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
