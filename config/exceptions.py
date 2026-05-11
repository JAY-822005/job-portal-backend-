"""
Custom exception handlers for the Job Portal API.
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides consistent error responses.
    """
    response = exception_handler(exc, context)

    if response is not None:
        # Add custom error formatting
        custom_response_data = {
            'success': False,
            'message': 'An error occurred',
            'error': response.data,
            'status_code': response.status_code,
        }

        if isinstance(response.data, dict):
            if 'detail' in response.data:
                custom_response_data['message'] = str(response.data['detail'])
            elif 'non_field_errors' in response.data:
                custom_response_data['message'] = str(response.data['non_field_errors'][0])

        response.data = custom_response_data

    else:
        # Log unhandled exceptions
        logger.error(f"Unhandled exception: {exc}", exc_info=True)

        response = Response(
            {
                'success': False,
                'message': 'Internal server error',
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response
