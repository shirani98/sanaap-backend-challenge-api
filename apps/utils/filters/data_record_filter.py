from rest_framework.filters import BaseFilterBackend
from django.db.models import Q


class DataRecordFilter(BaseFilterBackend):

    ALLOWED_ORDERING_FIELDS = {
        'title', '-title',
        'created_at', '-created_at',
        'updated_at', '-updated_at',
        'is_active', '-is_active',
    }

    def filter_queryset(self, request, queryset, view):
        search = request.query_params.get('search')
        is_active = request.query_params.get('is_active')
        created_at_after = request.query_params.get('created_at_after')
        created_at_before = request.query_params.get('created_at_before')
        ordering = request.query_params.get('ordering', '-created_at')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        if created_at_after:
            queryset = queryset.filter(created_at__date__gte=created_at_after)

        if created_at_before:
            queryset = queryset.filter(created_at__date__lte=created_at_before)

        if ordering in self.ALLOWED_ORDERING_FIELDS:
            queryset = queryset.order_by(ordering)

        return queryset
