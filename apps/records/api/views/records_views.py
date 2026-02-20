from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from apps.records.api.serializers import (
    DataRecordSerializer,
    RecordResponseSerializer,
    RecordListResponseSerializer,
    NotFoundResponseSerializer,
    DeletedResponseSerializer,
)
from apps.records.selectors import DataRecordSelector
from apps.records.services import DataRecordService
from apps.utils import BaseResponse, DataRecordFilter, StandardResultsPagination

_LIST_FILTER_PARAMS = [
    OpenApiParameter("search", OpenApiTypes.STR, description="Case-insensitive search in title or description."),
    OpenApiParameter("is_active", OpenApiTypes.BOOL, description="Filter by active status."),
    OpenApiParameter("created_at_after", OpenApiTypes.DATE, description="Include records created on or after this date (YYYY-MM-DD)."),
    OpenApiParameter("created_at_before", OpenApiTypes.DATE, description="Include records created on or before this date (YYYY-MM-DD)."),
    OpenApiParameter("ordering", OpenApiTypes.STR, description="Sort field. Options: title, -title, created_at, -created_at, updated_at, -updated_at, is_active, -is_active."),
    OpenApiParameter("page", OpenApiTypes.INT, description="Page number (default: 1)."),
    OpenApiParameter("page_size", OpenApiTypes.INT, description="Results per page (default: 10, max: 100)."),
]



class RecordListView(APIView):

    @extend_schema(
        tags=["Records"],
        summary="List records",
        parameters=_LIST_FILTER_PARAMS,
        responses={200: RecordListResponseSerializer},
    )
    def get(self, request):
        try:
            records = DataRecordSelector.get_all_records()
            records = DataRecordFilter().filter_queryset(request, records, self)

            paginator = StandardResultsPagination()
            page = paginator.paginate_queryset(records, request)
            serializer = DataRecordSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return BaseResponse.error(str(e))


class RecordCreateView(APIView):

    @extend_schema(
        tags=["Records"],
        summary="Create a record",
        request=DataRecordSerializer,
        responses={
            201: RecordResponseSerializer,
            400: NotFoundResponseSerializer,
        },
    )
    def post(self, request):
        try:
            serializer = DataRecordSerializer(data=request.data)
            if not serializer.is_valid():
                return BaseResponse.validation_error(serializer.errors)

            record = DataRecordService.create_record(
                title=serializer.validated_data.get('title'),
                description=serializer.validated_data.get('description', ''),
                file=serializer.validated_data.get('file', None),
                is_active=serializer.validated_data.get('is_active', True),
            )

            output_serializer = DataRecordSerializer(record)
            return BaseResponse.created(data=output_serializer.data)

        except ValidationError as e:
            return BaseResponse.error(str(e))


class RecordRetrieveView(APIView):

    @extend_schema(
        tags=["Records"],
        summary="Retrieve a record",
        responses={
            200: RecordResponseSerializer,
            404: NotFoundResponseSerializer,
        },
    )
    def get(self, request, pk):
        try:
            record = DataRecordSelector.get_record_by_id(pk)
            if not record:
                return BaseResponse.not_found()

            serializer = DataRecordSerializer(record)
            return BaseResponse.success(data=serializer.data)
        except Exception as e:
            return BaseResponse.error(str(e))


class RecordUpdateView(APIView):

    @extend_schema(
        tags=["Records"],
        summary="Partially update a record",
        request=DataRecordSerializer,
        responses={
            200: RecordResponseSerializer,
            404: NotFoundResponseSerializer,
        },
    )
    def patch(self, request, pk):
        try:
            record = DataRecordSelector.get_record_by_id(pk)
            if not record:
                return BaseResponse.not_found()

            serializer = DataRecordSerializer(data=request.data, partial=True)
            if not serializer.is_valid():
                return BaseResponse.validation_error(serializer.errors)

            updated_record = DataRecordService.update_record(pk, **serializer.validated_data)
            output_serializer = DataRecordSerializer(updated_record)
            return BaseResponse.success(data=output_serializer.data)

        except ValidationError as e:
            return BaseResponse.error(str(e))


class RecordDeleteView(APIView):

    @extend_schema(
        tags=["Records"],
        summary="Delete a record",
        responses={
            204: DeletedResponseSerializer,
            404: NotFoundResponseSerializer,
        },
    )
    def delete(self, request, pk):
        try:
            record = DataRecordSelector.get_record_by_id(pk)
            if not record:
                return BaseResponse.not_found()

            DataRecordService.delete_record(pk)
            return BaseResponse.deleted()

        except ValidationError as e:
            return BaseResponse.error(str(e))
