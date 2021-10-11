在[DRF框架初体验](http://www.panzhixiang.cn/article/2021/9/9/43.html)中其实已经使用了视图了（book.views里面的代码），而且就是实际开发中最常用的模式，但是那是经过DRF框架高度封装的，代码的可读性不好，而且如果不了解里面的细节，当以后遇到需要定制化的工作时可能就无从下手，这一篇笔记会记录一些我自己认为比较重要切常用的实现细节。

**写在前面：**
本文后面所有的代码样例中，book.urls里面，以下两段代码只能二选一，使用其中一个的时候必须把另外一个注释掉。  

**第一段是与ViewSet配置使用的，第二段是与ModelViewSet配置使用的。**  

```python
    url(r'^bookinfos/$', views.BookInfoViewSet.as_view({'get':'list', 'post':'create'})),
    url(r'^bookinfos/(?P<pk>\d+)$', views.BookInfoViewSet.as_view({'get':'retrieve', 'put':'update', 'delete':'delete'})),
    url(r'^bookinfos/latest/$', views.BookInfoViewSet.as_view({'get':'latest'})),
```

```python
router.register('bookinfos', views.BookInfoModelViewSet, basename='bookinfo')
```

# ModelViewSet
当视图有对应的Django Model（数据库模型类）的时候，最常用的就是ModelViewSet，因为DRF为我们封装了大量重复的事情，在实际开发工作中可以节省很多时间。  
以下是基于ModelViewSet实现视图类的代码：  

```python
class BookInfoModelViewSet(ModelViewSet):
    '''利用ModelViewSet实现图书信息视图，包含增删查改所有操作'''
    queryset = BookInfo.objects.all()  # 指定可以作用的数据范围
    serializer_class = BookInfoSerializer  # 指定序列化器
```  
可以看到一共只有三行代码，但是这三行代码实现了API里面的最常见的增删查改所有的功能，由此可见ModelViewSet确实非常高效。  
上面的视图类需要配合以下url代码才能正常工作。  

```python
# demo.urls，即项目根路由的配置如下
urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('book.urls') )
]

# book.urls, 即应用的路由如下
router = DefaultRouter()

router.register('bookinfos', views.BookInfoModelViewSet, basename='bookinfos')

urlpatterns = [
] + router.urls
```  
这样将Django Server运行起来后就可以在http://127.0.0.1:8000/books/ 路径下看到api清单了。  


# ViewSet
虽然ModelViewSet在配合Django的数据库模型类开发的时候非常高效，但是它并不适用于所有的场景，比如当后端没有对应数据库模型类的时候就是不能使用它了。  

下面是使用ViewSet实现视图类的代码，包含视图类代码本身和url配置代码，基于ViewSet实现的视图类，在url上有一些特定的配置。  

* **视图类代码**  

这里有一个特别的处理，就是视图类中的函数名是list, create这样具体的动作，而不是在django中的put，post这样的请求方法，这和后面的url中配置有关。  

在这个样例代码中，我依然使用到了Django的数据库模型类，但是其实如果把list、update这些函数内的代码换成其他的业务逻辑也是没有问题的，这样就是没有数据库模型类的使用场景。  

```python
class BookInfoViewSet(ViewSet):
    '''
    利用ViewSet实现图书信息视图类，包含增删查改四个功能，
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
        新增一条书本信息
        url类似于127.0.0.1:8000/books/bookinfos/
        '''
        serializer = BookInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        '''
        删除某一条书本信息,
        url类似于127.0.0.1:8000/books/bookinfos/
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
        更新某一条书本信息,
        url类似于127.0.0.1:8000/books/bookinfos/
        '''
        try:
            bookinfo = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookInfoSerializer(instance=bookinfo, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
```

* **url 配置**  

```python
router = DefaultRouter()

# router.register('bookinfos', views.BookInfoModelViewSet, basename='bookinfo')

urlpatterns = [
    # url(r'^$', views.BookListView.as_view()),
    # url(r'^(?P<pk>\d+)$', views.BookDetailView.as_view()),
    url(r'^bookinfos/$', views.BookInfoViewSet.as_view({'get':'list', 'post':'create'})),
    url(r'^bookinfos/(?P<pk>\d+)$', views.BookInfoViewSet.as_view({'get':'retrieve', 'put':'update', 'delete':'delete'}))
] + router.urls
```  
可以看到在与Django中不同的是，在视图类的as_view方法中添加了一个字典参数，字典中的内容是HTTP请求方法和对应的函数名的键值对。  

其中GET请求方法有两个函数，一个是list，一个是retrieve，分别是查所有记录和查单一记录，区别在于url最后有没有捕捉“pk”(主键)这个参数。

这里事实上是DRF框架对路由的分发机制在Django的基础上做了优化，让我们可以将所有的请求方法都写在一个视图类中，而不用像在Django中那样必须区分列表类视图还是详情类视图。在Django中，由于查单一和查多个都是由GET请求方法触发的，所以不能写在同一个类中，必须拆分到详情类和视图类中。  

# 实现自定义的API
上面两个案例中，不管是使用ModelViewSet还是ViewSet，实现的都是对数据库的增删查改这四种功能，但是实际开发过程中，往往还有其他一些比较复杂的场景，这个时候就需要自定义开发一些API了。  
这里以查询bookinfo表中最新的一本书（id最大的书）这个需求为例，分别使用ModelViewSet和ViewSet实现，  
* **基于ModelViewSet实现自定义API**

基于ModelViewSet实现自定义API其实就是在视图类中新增一个函数（这里是latest），然后用action作为装饰器，指定methods和detail这两个参数，对于url不需要做任何修改，但是如果是基于ViewSet实现自定义API的话就需要修改url中as_view的参数
```python
class BookInfoModelViewSet(ModelViewSet):
    '''利用ModelViewSet实现图书信息视图，包含增删查改所有操作'''
    queryset = BookInfo.objects.all()  # 指定可以作用的数据范围
    serializer_class = BookInfoSerializer  # 指定序列化器

    # methods表示请求方法；
    # detail表示是否为详情视图，简单来说就是需不需要id，
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
```

* **基于ViewSet实现自定义API**

基于ViewSet实现自定义API需要修改视图类和url两部分代码。  
其中视图类的修改就是在原来的基础上添加自定义的函数逻辑，这里就是latest函数。

```python
# 视图类代码
class BookInfoViewSet(ViewSet):
    '''
    利用ViewSet实现图书信息视图类，包含增删查改四个功能，
    这里有一个特别的处理，就是函数名是list, create这样具体的动作，
    而不是在django中的put，post这样的请求方法，
    这和后面的url中配置有关
    '''
    def list(self, request):
        pass
    
    def retrieve(self, request, pk):
        pass

    def create(self, request):
        pass

    def delete(self, request, pk):
        pass

    def update(self, request, pk):
        pass

    def latest(self, request):
        '''
        查询最新的图书信息
        '''
        bookinfo = BookInfo.objects.latest('id')
        serializer = BookInfoSerializer(bookinfo)

        return Response(serializer.data)
```

```python
# url 代码
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

# router.register('bookinfos', views.BookInfoModelViewSet, basename='bookinfo')

urlpatterns = [
    # url(r'^$', views.BookListView.as_view()),
    # url(r'^(?P<pk>\d+)$', views.BookDetailView.as_view()),
    url(r'^bookinfos/$', views.BookInfoViewSet.as_view({'get':'list', 'post':'create'})),
    url(r'^bookinfos/(?P<pk>\d+)$', views.BookInfoViewSet.as_view({'get':'retrieve', 'put':'update', 'delete':'delete'})),
    url(r'^bookinfos/latest/$', views.BookInfoViewSet.as_view({'get':'latest'})),

] + router.urls
```

url部分相较于之前，增加了下面这一行，其实就是新增一个url路径指向自定义的函数逻辑。  
```python
url(r'^bookinfos/latest/$', views.BookInfoViewSet.as_view({'get':'latest'})),
```

在ModelViewSet中，这一部分是利用action这个装饰器指定methods和detail这两个参数帮我们做掉了，所不用自己再去修改url。  

# 总结
可以看到，总的来说，ModelViewSet在有数据库模型类的情况还是比ViewSet好用很多的，但是当后端没有数据库模型类的时候，就只能使用ViewSet了，所谓我们对于这两个视图类都要有一定的掌握，才能应用日常的开发工作。  

其实ModelViewSet和ViewSet分别继承于GenericViewSet和APIView，上面说到的他们的不同点也正是源于此，建议读者可以看看rest_framework.viewsets里面的源码，里面详细地写明了从GenericViewSet和APIView发展到ModelViewSet和ViewSet的过程，有助于理解里面的细节，也能在以后开发中遇到问题的时候更容易debug。  
另外视图类的as_view方法决定了路由的分发机制，也是比较重要一个点。