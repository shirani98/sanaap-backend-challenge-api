from django.core.exceptions import ValidationError
from apps.records.models.records_model import DataRecord


class DataRecordService:

    @staticmethod
    def create_record(
        title: str,
        description: str = "",
        file = None,
        is_active: bool = True
    ) -> DataRecord:
        if not title or not title.strip():
            raise ValidationError("Title cannot be empty")

        if len(title) > 200:
            raise ValidationError("Title cannot exceed 200 characters")

        record = DataRecord.objects.create(
            title=title.strip(),
            description=description.strip() if description else "",
            file=file,
            is_active=is_active
        )
        return record

    @staticmethod
    def update_record(
        record_id: int,
        **kwargs
    ) -> DataRecord:
        try:
            record = DataRecord.objects.get(id=record_id)
        except DataRecord.DoesNotExist:
            raise ValidationError(f"Record with ID {record_id} not found")

        if 'title' in kwargs:
            title = kwargs['title']
            if not title or not title.strip():
                raise ValidationError("Title cannot be empty")
            if len(title) > 200:
                raise ValidationError("Title cannot exceed 200 characters")
            record.title = title.strip()

        if 'description' in kwargs:
            record.description = kwargs['description'].strip() if kwargs['description'] else ""

        if 'file' in kwargs:
            record.file = kwargs['file']

        if 'is_active' in kwargs:
            record.is_active = kwargs['is_active']

        record.save()
        return record

    @staticmethod
    def delete_record(record_id: int) -> bool:
        try:
            record = DataRecord.objects.get(id=record_id)
            record.delete()
            return True
        except DataRecord.DoesNotExist:
            raise ValidationError(f"Record with ID {record_id} not found")

    @staticmethod
    def toggle_record_active_status(record_id: int) -> DataRecord:
        try:
            record = DataRecord.objects.get(id=record_id)
        except DataRecord.DoesNotExist:
            raise ValidationError(f"Record with ID {record_id} not found")

        record.is_active = not record.is_active
        record.save()
        return record

    @staticmethod
    def bulk_update_active_status(record_ids: list[int], is_active: bool) -> int:
        if not record_ids:
            raise ValidationError("No record IDs provided")

        updated_count = DataRecord.objects.filter(
            id__in=record_ids
        ).update(is_active=is_active)

        return updated_count

    @staticmethod
    def bulk_delete_records(record_ids: list[int]) -> int:
        if not record_ids:
            raise ValidationError("No record IDs provided")

        deleted_count, _ = DataRecord.objects.filter(
            id__in=record_ids
        ).delete()

        return deleted_count
