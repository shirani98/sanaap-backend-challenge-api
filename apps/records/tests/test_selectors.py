from django.test import TestCase

from apps.records.models.records_model import DataRecord
from apps.records.selectors.records_selector import DataRecordSelector


class DataRecordSelectorTests(TestCase):

    def setUp(self):
        self.active = DataRecord.objects.create(title="Active Report", description="active", is_active=True)
        self.inactive = DataRecord.objects.create(title="Inactive Doc", description="inactive", is_active=False)

    def test_get_all_records_returns_all(self):
        self.assertEqual(DataRecordSelector.get_all_records().count(), 2)

    def test_get_all_active_records(self):
        qs = DataRecordSelector.get_all_active_records()
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), self.active)

    def test_get_all_inactive_records(self):
        qs = DataRecordSelector.get_all_inactive_records()
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), self.inactive)

    def test_get_record_by_id_exists(self):
        record = DataRecordSelector.get_record_by_id(self.active.id)
        self.assertEqual(record, self.active)

    def test_get_record_by_id_not_found(self):
        record = DataRecordSelector.get_record_by_id(9999)
        self.assertIsNone(record)

    def test_search_by_title(self):
        qs = DataRecordSelector.search_records("Report")
        self.assertIn(self.active, qs)
        self.assertNotIn(self.inactive, qs)

    def test_search_by_description(self):
        qs = DataRecordSelector.search_records("inactive")
        self.assertIn(self.inactive, qs)
