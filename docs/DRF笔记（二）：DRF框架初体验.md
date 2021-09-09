[DRF笔记（一）：手工实现常见API ](http://www.panzhixiang.cn/article/2021/9/8/42.html) 中记录了如何手工基于Django实现常见的API类型，这篇笔记记录一下DRF框架简单使用的体验。  

笔记中提到的代码repo：[https://github.com/yexia553/drf](https://github.com/yexia553/drf)

# 安装和配置修改
* 安装DRF
安装drf之前要先安装Django  
```sh
pip install djangorestframework
``` 

* 修改Django的settings.py文件
将’rest_framework’添加到‘INSTALLED_APPS’中，如下  
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

# 编写序列化器
序列化和反序列化的意思其实就是利用Django的Model将数据库中的数据进行一定的格式修改（比如dict变成json）之后返回给api请求者和将从api请求获取到的数据写入到数据库的过程。 

在’book’ app中新建serializers.py文件，文件内容如下：
```python
from rest_framework import serializers
from .models import BookInfo


class BookInfoSerializer(serializers.ModelSerializer):
    """定义序列化器"""
    class Meta:
        model = BookInfo  # 指定作用的模型
        fields = '__all__'  # 指定序列化的字段，这里让所有字段都能被序列化
```
上面这一段代码的作用其实就是代替了我在手工实现API的时候反复写的利用model从数据库获取数据和将从api获取到的数据写入数据库的过程，下面列举了一个查询某一本具体的书的例子。  
```python
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
```  

# 编写视图
在book 的view.py里面新增一个视图类，如下：  
```python
from rest_framework.viewsets import ModelViewSet


class BookInfoView(ModelViewSet):
    '''图书信息视图，包含增删查改所有操作'''
    queryset = BookInfo.objects.all()  # 指定可以作用的数据范围

    serializer_class = BookInfoSerializer  # 指定序列化器
```
上面这个视图类只有三行，但是它却实现了笔记一中BookListView和BookDetailView两个视图类所有的功能，由此可以见DRF框架还是很方便的，减少了很多重复代码的编写工作。  

# 修改url配置
1. demo中的跟路由配置可以不作任何修改  
如下：  
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('book.urls') )
]
```
以books/开头的url会导向book app中的路由

2. book中url修改  
修改book/urls.py如下：  
```python
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()  # DefaultRouter会帮助生成api的路由

# 第一个参数是路由，这里置空，这样配合跟路由中的配置，
#就可以实现http://127.0.0.1/books/ 指向views.BookInfoView，
router.register('', views.BookInfoView, basename='books')

# Django只会在urlpatterns中寻找路由，所以要把上面配置生成的url加到urlpatterns中
urlpatterns = [
    # url(r'^$', views.BookListView.as_view()),
    # url(r'^(?P<pk>\d+)$', views.BookDetailView.as_view()),
] + router.urls
```

# 测试
* 通过浏览器测试
将项目运行起来之后，在浏览器分别输入一下地址：  
  1. http://127.0.0.1:8000/books/  
  * 这个url就是查询所有书籍信息的API，可以在浏览器中看到当前数据中的数据；  
  * 页面的最下面是一个表格，右下角有一个POST按钮，这个按钮对应的是POST API，也就是创建一本书
  2. http://127.0.0.1:8000/books/2
  * 当在浏览器中输入这个url的时候，实际上也是一个查询的API，但是是查询id为2的这一本书的信息；  
  * 不过当进入之后会看到页面右上角会有一个红色的DELETE按钮，这个按钮对应的就是DELETE API；  
  * 页面的下半部分是一个表格，右下角有一个蓝色的PUT按钮，这个按钮对应的就是PUT API；  
</br>

* 通过代码测试
test路径下有一个文件drf_first_seen.py,运行这个文件，会返回每一个API测试成功或者的结果，如下：  
```sh
(venv): python drf_first_seen.py 
测试查询具体书本信息API成功
测试创建书本API成功
测试查询所有书本信息API成功
测试更新API成功
测试删除API成功
```

