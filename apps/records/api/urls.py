from django.urls import path
from apps.records.api.views import (
    RecordListView,
    RecordCreateView,
    RecordRetrieveView,
    RecordUpdateView,
    RecordDeleteView,
)


class RecordListCreateView(RecordListView, RecordCreateView):
    """GET + POST  /api/records/"""


class RecordDetailView(RecordRetrieveView, RecordUpdateView, RecordDeleteView):
    """GET + PUT + PATCH + DELETE  /api/records/<pk>/"""


urlpatterns = [
    path('records/', RecordListCreateView.as_view(), name='record-list-create'),
    path('records/<int:pk>/', RecordDetailView.as_view(), name='record-detail'),
]
