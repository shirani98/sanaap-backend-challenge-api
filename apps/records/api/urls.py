from django.urls import path
from apps.records.api.views import (
    RecordListView,
    RecordCreateView,
    RecordRetrieveView,
    RecordUpdateView,
    RecordDeleteView,
)





urlpatterns = [
    path('records/', RecordListView.as_view(), name='record-list'),
    path('records/create/', RecordCreateView.as_view(), name='record-create'),
    path('records/<int:pk>/', RecordRetrieveView.as_view(), name='record-detail'),
    path('records/<int:pk>/update/', RecordUpdateView.as_view(), name='record-update'),
    path('records/<int:pk>/delete/', RecordDeleteView.as_view(), name='record-delete'),
]
