from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from apps.records.api.serializers import DataRecordSerializer
from apps.records.selectors import DataRecordSelector
from apps.records.services import DataRecordService
from apps.utils import BaseResponse, DataRecordFilter, StandardResultsPagination


class RecordListView(APIView):

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

    def put(self, request, pk):
        try:
            record = DataRecordSelector.get_record_by_id(pk)
            if not record:
                return BaseResponse.not_found()

            serializer = DataRecordSerializer(data=request.data)
            if not serializer.is_valid():
                return BaseResponse.validation_error(serializer.errors)

            updated_record = DataRecordService.update_record(pk, **serializer.validated_data)
            output_serializer = DataRecordSerializer(updated_record)
            return BaseResponse.success(data=output_serializer.data)

        except ValidationError as e:
            return BaseResponse.error(str(e))

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

    def delete(self, request, pk):
        try:
            record = DataRecordSelector.get_record_by_id(pk)
            if not record:
                return BaseResponse.not_found()

            DataRecordService.delete_record(pk)
            return BaseResponse.deleted()

        except ValidationError as e:
            return BaseResponse.error(str(e))
