"""
GET    /books/   查询所有记录
POST   /books/   增加一条记录
GET    /books/id 查询某一条记录
PUT    /books/id 修改某一条记录
DELETE /books/id 删除某一条记录
修改其实还有一个PATCH，比较麻烦，不写了
"""
from decimal import DecimalException
from django.http.response import HttpResponse
from django.views import View
from django.http import JsonResponse
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import BookInfo, HeroInfo
from .serializers import BookInfoSerializer, HeroInfoSerializer
from demo.utils.permissions import HasGroupPermission
import json
from .filters import BookInfoFilter


class BookInfoModelViewSet(ModelViewSet):
    '''利用ModelViewSet实现图书信息视图，包含增删查改所有操作'''
    queryset = BookInfo.objects.all()  # 指定可以作用的数据范围
    serializer_class = BookInfoSerializer  # 指定序列化器
    ordering_fields = ('id', 'title') # 指定排序的字段，这样可以在请求中对这些字段进行排序
    filter_class = BookInfoFilter
    
    # methods表示请求方法；
    # detail表示是否为详情视图，简单来说就是需要不要id，
    # 如果需要id,detail就为True，否则为False，
    # 在这个例子中，不需要id，所以为False
    @action(methods=['get'], detail=False)  
    def latest(self, request):
        '''
        查询最新的图书信息
        '''
        bookinfo = BookInfo.objects.latest('id')
        serializer = self.get_serializer(bookinfo)

        return Response(serializer.data)


class HeroInfoModelViewSet(ModelViewSet):
    '''利用ModelViewSet实现英雄信息视图'''
    queryset = HeroInfo.objects.all()
    serializer_class = HeroInfoSerializer
    ordering_fields = ['id', 'name']  # 指定可以用于排序的字段
    filter_fields = ['id', 'name']  # 指定可以用于过滤的字段



class BookInfoViewSet(ViewSet):
    '''
    利用ViewSet实现图书信息视图类，包含增删查改四个功能，
    这里有一个特别的处理，就是函数名是list, create这样具体的动作，
    而不是在django中的put，post这样的请求方法，
    这和后面的url中配置有关
    '''
    def list(self, request):
        '''
        查寻多个书本信息，
        url类似于127.0.0.1:8000/books/bookinfos/
        '''
        bookinfos = BookInfo.objects.all()
        serializer = BookInfoSerializer(instance=bookinfos, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        '''
        查询某一个具体的书本信息
        url类似于127.0.0.1:8000/books/bookinfos/id;
        相对于 查询多个 ，在url的最后多个id（主键）
        '''
        try:
            bookinfo = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BookInfoSerializer(instance=bookinfo)
        return Response(serializer.data)

    def create(self, request):
        '''
        新增一条书本信息,
        url类似于127.0.0.1:8000/books/bookinfos/
        '''
        serializer = BookInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        '''
        删除某一条书本信息
        url类似于127.0.0.1:8000/books/bookinfos/id
        '''
        try:
            bookinfo = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        bookinfo.is_delete = True  # 逻辑删除
        bookinfo.save()
        return Response(status=status.HTTP_200_OK)

    def update(self, request, pk):
        '''
        更新某一条书本信息
        url类似于127.0.0.1:8000/books/bookinfos/id
        '''
        try:
            bookinfo = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookInfoSerializer(instance=bookinfo, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def latest(self, request):
        '''
        查询最新的图书信息
        '''
        bookinfo = BookInfo.objects.latest('id')
        serializer = BookInfoSerializer(bookinfo)

        return Response(serializer.data)

# class BookListView(View):
#     """
#     手工实现图书列表视图
#     """
#     def get(self, request):
#         """查询所有图书"""
#         books = BookInfo.objects.all()
#         res = list()
#         for book in books:
#             bookinfo = {
#                 'id': book.id,
#                 'title': book.title,
#                 'pub_date': book.pub_date,
#                 'comment': book.comment,
#                 'read': book.read,
#                 'image': book.image.url if book.image else ''
#             }
#             res.append(bookinfo)
#         return JsonResponse(res, safe=False)

#     def post(self, request):
#         '''新增一本图书信息'''
#         body = request.body.decode()
#         body = json.loads(body)
#         book = BookInfo(
#             title=body['title'],
#             pub_date=body['pub_date'],
#             comment=body['comment'],
#             read=body['read']
#         )
#         book.save()
#         res = {
#             'id': book.id,
#             'title': book.title,
#             'pub_date': book.pub_date,
#             'comment': book.comment,
#             'read': book.read,
#             'image': book.image.url if book.image else ''
#         }
#         # 返回新创建的图书的信息，以及201状态码
#         return JsonResponse(res, status=201)


# class BookDetailView(View):
#     """
#     手工实现图书信息详情视图
#     """
#     def get(self, request, pk):
#         '''查询某一本书的详细信息'''
#         try:
#             book = BookInfo.objects.get(id=pk)
#         except BookInfo.DoesNotExist:
#             return HttpResponse({'mesage':'查询的数据不存在'}, status=404)
        
#         res = {
#             'id': book.id,
#             'title': book.title,
#             'read': book.read,
#             'pub_date': book.pub_date,
#             'comment': book.comment,
#             'image': book.image.url if book.image else ''
#         }

#         return JsonResponse(res)
    
#     def put(self, request, pk):
#         '''修改一本的数据'''
#         # 先查询要修改的数据是否存在
#         try:
#             book = BookInfo.objects.get(id=pk)
#         except BookInfo.DoesNotExist:
#             return HttpResponse({'mesage':'要修改的数据不存在'}, status=404)
#         # 获取请求中的数据
#         body = request.body.decode()
#         body = json.loads(body)
#         # 修改数据并保存
#         book.title=body['title'],
#         book.pub_date=body['pub_date'],
#         book.comment=body['comment'],
#         book.read=body['read']
#         book.save()
#         # 构造返回数据
#         res = {
#             'id': book.id,
#             'title': book.title,
#             'read': book.read,
#             'pub_date': book.pub_date,
#             'comment': book.comment,
#             'image': book.image.url if book.image else ''
#         }
#         return HttpResponse(res)

#     def delete(self, request, pk):
#         '''删除一本书'''
#         try:
#             book = BookInfo.objects.get(id=pk)
#         except BookInfo.DoesNotExist:
#             return HttpResponse({'mesage':'要删除的数据不存在'}, status=404)
#         book.is_delete = True  # 逻辑删除
#         book.save()
#         # 删除可以没有响应体，只给出204状态码
#         return HttpResponse(status=204)


