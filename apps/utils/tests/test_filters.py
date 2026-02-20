from django.test import TestCase, RequestFactory

from apps.records.models.records_model import DataRecord
from apps.utils.filters.data_record_filter import DataRecordFilter


class DataRecordFilterTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.filter = DataRecordFilter()
        self.qs = DataRecord.objects.all()

        DataRecord.objects.create(title="Annual Report", description="finance", is_active=True)
        DataRecord.objects.create(title="Project Plan", description="planning report", is_active=False)
        DataRecord.objects.create(title="Meeting Notes", description="notes", is_active=True)

    def _filter(self, params):
        request = self.factory.get("/", params)
        return self.filter.filter_queryset(request, DataRecord.objects.all(), view=None)

    def test_search_matches_title(self):
        qs = self._filter({"search": "Annual"})
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first().title, "Annual Report")

    def test_search_matches_description(self):
        qs = self._filter({"search": "planning"})
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first().title, "Project Plan")

    def test_search_no_match_returns_empty(self):
        qs = self._filter({"search": "xyz_nomatch"})
        self.assertEqual(qs.count(), 0)

    def test_filter_active_true(self):
        qs = self._filter({"is_active": "true"})
        self.assertTrue(all(r.is_active for r in qs))

    def test_filter_active_false(self):
        qs = self._filter({"is_active": "false"})
        self.assertTrue(all(not r.is_active for r in qs))

    def test_ordering_by_title(self):
        qs = self._filter({"ordering": "title"})
        titles = list(qs.values_list("title", flat=True))
        self.assertEqual(titles, sorted(titles))

    def test_invalid_ordering_falls_back_to_default(self):
        # Should not raise; falls back to model default ordering
        qs = self._filter({"ordering": "invalid_field"})
        self.assertEqual(qs.count(), 3)
