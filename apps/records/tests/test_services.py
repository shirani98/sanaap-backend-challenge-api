from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.records.models.records_model import DataRecord
from apps.records.services.records_service import DataRecordService


class CreateRecordTests(TestCase):

    def test_creates_with_valid_data(self):
        record = DataRecordService.create_record(title="Report", description="desc")
        self.assertEqual(record.title, "Report")
        self.assertEqual(record.description, "desc")
        self.assertTrue(record.is_active)

    def test_strips_whitespace_from_title(self):
        record = DataRecordService.create_record(title="  Report  ")
        self.assertEqual(record.title, "Report")

    def test_raises_if_title_empty(self):
        with self.assertRaises(ValidationError):
            DataRecordService.create_record(title="")

    def test_raises_if_title_only_spaces(self):
        with self.assertRaises(ValidationError):
            DataRecordService.create_record(title="   ")

    def test_raises_if_title_too_long(self):
        with self.assertRaises(ValidationError):
            DataRecordService.create_record(title="x" * 201)

    def test_is_active_defaults_to_true(self):
        record = DataRecordService.create_record(title="T")
        self.assertTrue(record.is_active)

    def test_creates_inactive_record(self):
        record = DataRecordService.create_record(title="T", is_active=False)
        self.assertFalse(record.is_active)


class UpdateRecordTests(TestCase):

    def setUp(self):
        self.record = DataRecord.objects.create(title="Original", description="desc")

    def test_updates_title(self):
        updated = DataRecordService.update_record(self.record.id, title="Updated")
        self.assertEqual(updated.title, "Updated")

    def test_updates_is_active(self):
        updated = DataRecordService.update_record(self.record.id, is_active=False)
        self.assertFalse(updated.is_active)

    def test_raises_for_nonexistent_record(self):
        with self.assertRaises(ValidationError):
            DataRecordService.update_record(9999, title="X")

    def test_raises_if_title_set_to_empty(self):
        with self.assertRaises(ValidationError):
            DataRecordService.update_record(self.record.id, title="")


class DeleteRecordTests(TestCase):

    def setUp(self):
        self.record = DataRecord.objects.create(title="To Delete")

    def test_deletes_existing_record(self):
        DataRecordService.delete_record(self.record.id)
        self.assertFalse(DataRecord.objects.filter(id=self.record.id).exists())

    def test_raises_for_nonexistent_record(self):
        with self.assertRaises(ValidationError):
            DataRecordService.delete_record(9999)


class ToggleActiveTests(TestCase):

    def test_toggles_active_to_inactive(self):
        record = DataRecord.objects.create(title="T", is_active=True)
        result = DataRecordService.toggle_record_active_status(record.id)
        self.assertFalse(result.is_active)

    def test_toggles_inactive_to_active(self):
        record = DataRecord.objects.create(title="T", is_active=False)
        result = DataRecordService.toggle_record_active_status(record.id)
        self.assertTrue(result.is_active)


class BulkOperationTests(TestCase):

    def setUp(self):
        self.r1 = DataRecord.objects.create(title="A", is_active=True)
        self.r2 = DataRecord.objects.create(title="B", is_active=True)

    def test_bulk_delete(self):
        count = DataRecordService.bulk_delete_records([self.r1.id, self.r2.id])
        self.assertEqual(count, 2)
        self.assertEqual(DataRecord.objects.count(), 0)

    def test_bulk_update_status(self):
        DataRecordService.bulk_update_active_status([self.r1.id, self.r2.id], False)
        self.assertFalse(DataRecord.objects.get(id=self.r1.id).is_active)
        self.assertFalse(DataRecord.objects.get(id=self.r2.id).is_active)
