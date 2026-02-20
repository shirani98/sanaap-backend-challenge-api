from rest_framework import serializers
from apps.records.models.records_model import DataRecord


class DataRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataRecord
        fields = ['id', 'title', 'description', 'file', 'created_at', 'updated_at', 'is_active']
        read_only_fields = ['id', 'created_at', 'updated_at']
