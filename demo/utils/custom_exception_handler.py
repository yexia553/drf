from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status
from rest_framework.response import Response
from django.db import DatabaseError


def exception_handler(exc, context):
    '''
    在drf原本捕捉异常能力的基础上添加自定义的异常捕捉
    '''
    response = drf_exception_handler(exc, context)

    # 自定义数据库异常捕捉
    if response is None:
        if isinstance(exc, DatabaseError):
            response = Response({'detail:数据库错误！'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
