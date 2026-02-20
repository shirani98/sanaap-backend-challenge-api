from django.db.models import QuerySet
from apps.records.models.records_model import DataRecord


class DataRecordSelector:

    @staticmethod
    def get_all_records() -> QuerySet:
        return DataRecord.objects.all()

    @staticmethod
    def get_all_active_records() -> QuerySet:
        return DataRecord.objects.filter(is_active=True)

    @staticmethod
    def get_all_inactive_records() -> QuerySet:
        return DataRecord.objects.filter(is_active=False)

    @staticmethod
    def get_record_by_id(record_id: int) -> DataRecord | None:
        try:
            return DataRecord.objects.get(id=record_id)
        except DataRecord.DoesNotExist:
            return None

    @staticmethod
    def search_records(query: str) -> QuerySet:
        return DataRecord.objects.filter(
            title__icontains=query
        ) | DataRecord.objects.filter(
            description__icontains=query
        )

    @staticmethod
    def get_records_by_activity_status(is_active: bool) -> QuerySet:
        return DataRecord.objects.filter(is_active=is_active)

    @staticmethod
    def get_records_ordered(ordering_field: str = '-created_at') -> QuerySet:
        allowed_fields = ['created_at', '-created_at', 'updated_at', '-updated_at', 'title', '-title']
        if ordering_field not in allowed_fields:
            ordering_field = '-created_at'
        return DataRecord.objects.all().order_by(ordering_field)
