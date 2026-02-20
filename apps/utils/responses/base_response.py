from rest_framework.response import Response
from rest_framework import status


class BaseResponse:

    @staticmethod
    def success(data=None, message=None, status_code=status.HTTP_200_OK):
        response_data = {
            'success': True,
            'message': message or 'Operation successful',
        }
        if data is not None:
            response_data['data'] = data
        return Response(response_data, status=status_code)

    @staticmethod
    def created(data=None, message=None):
        return BaseResponse.success(
            data=data,
            message=message or 'Resource created successfully',
            status_code=status.HTTP_201_CREATED
        )

    @staticmethod
    def deleted(message=None):
        return Response(
            {
                'success': True,
                'message': message or 'Resource deleted successfully',
            },
            status=status.HTTP_204_NO_CONTENT
        )

    @staticmethod
    def error(message, status_code=status.HTTP_400_BAD_REQUEST, errors=None):
        response_data = {
            'success': False,
            'message': message,
        }
        if errors is not None:
            response_data['errors'] = errors
        return Response(response_data, status=status_code)

    @staticmethod
    def not_found(message=None):
        return BaseResponse.error(
            message=message or 'Resource not found',
            status_code=status.HTTP_404_NOT_FOUND
        )

    @staticmethod
    def bad_request(message=None, errors=None):
        return BaseResponse.error(
            message=message or 'Invalid request',
            status_code=status.HTTP_400_BAD_REQUEST,
            errors=errors
        )

    @staticmethod
    def validation_error(errors, message=None):
        return BaseResponse.error(
            message=message or 'Validation error',
            status_code=status.HTTP_400_BAD_REQUEST,
            errors=errors
        )
