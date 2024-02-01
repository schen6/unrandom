from functools import wraps
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, APIException
from django.core.exceptions import PermissionDenied
import logging


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        error_message = response.data.get('detail', str(response.data))
        status_code = response.status_code

        return Response({
            "status": "error",
            "code": status_code,
            "message": error_message
        }, status=status_code)
    else:
        return Response({
            "status": "error",
            "code": 500,
            "message": "Internal Server Error"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def is_success_status(status_code):
    return 200 <= status_code < 300



def standardize_api_response(api_func):
    @wraps(api_func)
    def wrapper(request, *args, **kwargs):
        try:
            result = api_func(request, *args, **kwargs)
            status_code = result.status_code if isinstance(result, Response) else status.HTTP_200_OK
            response_data = {"status": "success" if is_success_status(status_code) else "error", "code": status_code}

            if not is_success_status(status_code):
                error_messages = [str(msg) for msgs in result.data.values() for msg in msgs] if isinstance(result.data, dict) else ["Error occurred"]
                response_data["message"] = error_messages if len(error_messages) > 1 else error_messages[0]
            else:
                response_data["data"] = result.data if isinstance(result, Response) else result

            return Response(response_data, status=status_code)

        except ValidationError as e:
            logging.error(f"Validation Error: {e.detail}")
            return Response({
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            logging.error(f"Permission Denied: {e}")
            return Response({
                "status": "error",
                "code": status.HTTP_403_FORBIDDEN,
                "message": str(e)
            }, status=status.HTTP_403_FORBIDDEN)

    return wrapper
