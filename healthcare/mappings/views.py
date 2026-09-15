from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import PatientDoctorMapping
from .serializers import MappingSerializer


class MappingViewSet(viewsets.ModelViewSet):
    serializer_class = MappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(patient__created_by=self.request.user)

    def retrieve(self, request, pk=None):
        # pk here is actually a patient_id per the spec's URL semantics
        mappings = self.get_queryset().filter(patient_id=pk)
        serializer = self.get_serializer(mappings, many=True)
        return Response(serializer.data)