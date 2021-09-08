# Django REST Framework
Django本身是一个前后端不分离的框架，适合很多相对简单的开发需求，但是现在很多场景比较复杂，尤其是前端比较复杂，而现在很多前端框架都很不错，能极大简化前端开发工作，这个时候前后端分离就很有必要了；而且现在一般团队中开发成员也都是前后端分离的，前端专门开发UI，后端专门开发业务逻辑；再加上微服务的流行，后端API化的趋势已经很明显了。  
Django REST Framework就是一个基于Django的前后端分离框架，可以将后端的功能封装成API对外提供服务。  


# 手工实现API
虽然drf可以很好地实现API，但是手动写一遍可以帮助理解drf到底做了哪些事情。  
常见的API有以下几种：  

|方法| url|动作|
|---|---|---|  
|GET    |/books/   |查询所有记录|
|POST   |/books/   |增加一条记录|
|GET    |/books/id |查询某一条记录|
|PUT    |/books/id |修改某一条记录|
|DELETE |/books/id |删除某一条记录|
修改其实还有一个PATCH，比较麻烦，不写了

上面几种总结下来其实就是：增删查改。  
但是查有两种情况: 一个是查一条具体的数据（url最后以id结尾），一个是查所有的数据（url最后以资源名结尾，比如/books）  

这篇笔记相关的代码在**mannual-api**分支上  
代码仓库：[https://github.com/yexia553/drf](https://github.com/yexia553/drf)

项目以一个记录书本信息和书中人物信息的应用为基础。  
一共有两张表，books和heros。  
 books表中包含一些与书籍相关的信息，比如阅读量、出版时间等；  
 heros表中包含一些人物相关的信息，比如性别、属于哪本书等。

### 项目结构
.
├── book--------------------Django应用，测试项目主要在这个目录中
├── db.sqlite3--------------数据库文件
├── demo--------------------Django项目目录
├── docs--------------------笔记目录
├── manage.py
├── README.md
├── requirements.txt
├── test--------------------测试代码目录，部分功能提供了现成的测试代码，直接运行即可
└── venv

### 代码解释（手工实现API）
在代码里面分类列表视图和详情视图两种。  
简单说，当url最后是以id结尾的就会走到详情视图（处理的是某一条具体的数据，如/books/10, 处理第10本书，查询、修改或者删除）；当url最后是以资源名结尾的就会走到列表视图（如/books/, 查询所有的书或者新建一本书等等）。  

* **列表视图 /books/**
```python
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
        '''新增一本图书'''
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
```

* **详情视图 /books/id**
```python
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
```

上面的列表视图和详情视图这两段代码，其实就是只利用Django做Web开发的时候常见操作，在View中利用Model对数据库进行增删查改操作，只是最终返回的是数据，而不是通过Template渲染过的页面，这样就和DRF的API能力非常相似

* **url解释**

跟路由(demo路径下urls.py)  
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('book.urls') )
]
```
应用路由（book目录下的urls.py）
```python
urlpatterns = [
    url(r'^$', BookListView.as_view()),
    url(r'^(?P<pk>\d+)$', BookDetailView.as_view()),
]
```
根据两段路由代码看，当访问http://127.0.0.1:8080/books/的时候会由列表视图（BookListView）处理，只有查询所有图书和新建图书这两种情况； 当访问http://127.0.0.1:8080/books/**id** 的时候由详情视图处理（BookDetailView）处理请求，有查询某一本具体的书、修改某一本书、删除一本书这三种情况。

* **测试**
test路径下有个文件：mannual_api.py  
里面写了POST和DELETE两种API的测试代码，直接运行即可，会返回测试成功或者失败的提示
```sh
$ python ./test/mannul_api.py 
资源创建成功，POST API测试成功
b'{"id": 10, "title": "\\u6597\\u7f57\\u5927\\u9646", "pub_date": "2015-12-12", "comment": "200", "read": "100", "image": ""}'
资源删除成功，DELETE API测试成功
```