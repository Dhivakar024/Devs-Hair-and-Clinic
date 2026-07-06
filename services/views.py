from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.permissions import IsStaffUser
from .models import Service


def service_to_dict(s: Service):
    return {
        "id": str(s.id),
        "name": s.name,
        "category": s.category,
        "description": s.description,
        "price": float(s.price),
        "duration_mins": s.duration_mins,
        "image_url": s.image_url,
        "active": s.active,
    }


class ServiceListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsStaffUser()]
        return []

    def get(self, request):
        services = Service.objects(active=True)
        return Response([service_to_dict(s) for s in services])

    def post(self, request):
        data = request.data
        if not data.get("name") or data.get("price") is None:
            return Response({"error": "name and price are required"}, status=400)
        service = Service(
            name=data["name"],
            category=data.get("category", ""),
            description=data.get("description", ""),
            price=data["price"],
            duration_mins=data.get("duration_mins", 30),
            image_url=data.get("image_url", ""),
        )
        service.save()
        return Response(service_to_dict(service), status=status.HTTP_201_CREATED)


class ServiceDetailView(APIView):
    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            return [IsStaffUser()]
        return []

    def get_object(self, pk):
        try:
            return Service.objects.get(id=pk)
        except Service.DoesNotExist:
            return None

    def get(self, request, pk):
        service = self.get_object(pk)
        if not service:
            return Response({"error": "Not found"}, status=404)
        return Response(service_to_dict(service))

    def put(self, request, pk):
        service = self.get_object(pk)
        if not service:
            return Response({"error": "Not found"}, status=404)
        data = request.data
        for field in ["name", "category", "description", "price", "duration_mins", "image_url", "active"]:
            if field in data:
                setattr(service, field, data[field])
        service.save()
        return Response(service_to_dict(service))

    def delete(self, request, pk):
        service = self.get_object(pk)
        if not service:
            return Response({"error": "Not found"}, status=404)
        service.active = False
        service.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
