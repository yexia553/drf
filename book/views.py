"""
GET    /books/   查询所有记录
POST   /books/   增加一条记录
GET    /books/id 查询某一条记录
PUT    /books/id 修改某一条记录
DELETE /books/id 删除某一条记录
修改其实还有一个PATCH，比较麻烦，不写了
"""
from django.http.response import HttpResponse
from django.views import View
from django.http import JsonResponse
from .models import BookInfo, HeroInfo
import json


class BookListView(View):
    """
    图书列表视图
    """
    def get(self, request):
        """查询所有图书"""
        books = BookInfo.objects.all()
        res = list()
        for book in books:
            bookinfo = {
                'id': book.id,
                'title': book.title,
                'pub_date': book.pub_date,
                'comment': book.comment,
                'read': book.read,
                'image': book.image.url if book.image else ''
            }
            res.append(bookinfo)
        return JsonResponse(res, safe=False)

    def post(self, request):
        '''新增一本图书信息'''
        body = request.body.decode()
        body = json.loads(body)
        book = BookInfo(
            title=body['title'],
            pub_date=body['pub_date'],
            comment=body['comment'],
            read=body['read']
        )
        book.save()
        res = {
            'id': book.id,
            'title': book.title,
            'pub_date': book.pub_date,
            'comment': book.comment,
            'read': book.read,
            'image': book.image.url if book.image else ''
        }
        # 返回新创建的图书的信息，以及201状态码
        return JsonResponse(res, status=201)


class BookDetailView(View):
    """
    图书信息详情视图
    """
    def get(self, request, pk):
        '''查询某一本书的详细信息'''
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse({'mesage':'查询的数据不存在'}, status=404)
        
        res = {
            'id': book.id,
            'title': book.title,
            'read': book.read,
            'pub_date': book.pub_date,
            'comment': book.comment,
            'image': book.image.url if book.image else ''
        }

        return JsonResponse(res)
    
    def put(self, request, pk):
        '''修改一本的数据'''
        # 先查询要修改的数据是否存在
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse({'mesage':'要修改的数据不存在'}, status=404)
        # 获取请求中的数据
        body = request.body.decode()
        body = json.loads(body)
        # 修改数据并保存
        book.title=body['title'],
        book.pub_date=body['pub_date'],
        book.comment=body['comment'],
        book.read=body['read']
        book.save()
        # 构造返回数据
        res = {
            'id': book.id,
            'title': book.title,
            'read': book.read,
            'pub_date': book.pub_date,
            'comment': book.comment,
            'image': book.image.url if book.image else ''
        }
        return HttpResponse(res)

    def delete(self, request, pk):
        '''删除一本书'''
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse({'mesage':'要删除的数据不存在'}, status=404)
        book.is_delete = True  # 逻辑删除
        book.save()
        # 删除可以没有响应体，只给出204状态码
        return HttpResponse(status=204)


