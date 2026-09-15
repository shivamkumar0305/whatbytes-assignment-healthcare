from rest_framework import serializers
from .models import PatientDoctorMapping
from patients.models import Patient
from doctors.models import Doctor


class MappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctorMapping
        fields = ["id", "patient", "doctor", "assigned_at"]

    def validate_patient(self, value):
        request = self.context["request"]
        if value.created_by != request.user:
            raise serializers.ValidationError("You can only assign doctors to your own patients.")
        return value