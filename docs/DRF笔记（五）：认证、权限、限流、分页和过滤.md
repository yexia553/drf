**写在前面**  
以下提到的代码的代码仓库：[https://github.com/yexia553/drf](https://github.com/yexia553/drf)  
分支： others


# 认证和权限
在实际开发中，认证这一部分常常是使用jwt，但jwt是相对独立并且比较复杂的模块，这里就不过多记录，以后有机会专门写一下jwt和drf的配合使用。  

认证部分的配置代码只要修改demo.settings就行了，具体如下：  

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',   # 基本认证
        'rest_framework.authentication.SessionAuthentication',  # session认证
    ),
}
```  
</br>

认证是和权限控制配合的，光有认证没什么用，关于DRF中的权限控制以前写过一篇很详细的笔记可以参考：[DRF中基于组的权限控制](http://www.panzhixiang.cn/article/2021/8/23/38.html) 

需要补充的是，除了上面的连接中提到的权限控制方法，一般还是会在配置文件中添加一个基础的权限控制策略，以让其全局生效，这个策略一般选择IsAuthenticated, 如下代码所示：  

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ( # 权限控制类别
        'rest_framework.permissions.IsAuthenticated',
    ),
}
```  
这表示只有登录的用户才能访问API，这样可以在一定程度防止匿名用户恶意获取我们的数据，但是也不是绝对的，比如注册页面、登录页面这些肯定不能要求用户登录后才能访问，不然就陷入死循环了。这个时候就可以通过在视图类中指定permission_classes来修改适用的权限控制策略。  
    
# 限流
限流指的是对用户请求的API的次数进行限制，目前我在实际开发中用的不多，所以以下内容不一定准确。  

限流一般有两种方法，一是对API进行限流，而是对视图进行限流。 

* **对API进行限流**  

首先需要在项目的settings中的rest_framework部分添加DEFAULT_THROTTLE_CLASSES和DEFAULT_THROTTLE_RATES，如下：  

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '100/minute'
    }
}
```
其中AnonRateThrottle表示对未认证用户进行限流，是通过不同的IP来区分不同的用户的，UserRateThrottle是对认证用户进行限流，通过id来区分不同的用户。  
这里设置为未认证用户每天100次请求次数，认证用户每分钟100次请求次数。

* **对视图进行限流**
也可以通过ScopedRateThrottle对视图进行限流，以下是示例代码，代码仓库中并没有。  

视图类代码：  

```python
class ContactDetailView(APIView):
    throttle_scope = 'contacts'  # 手动指定throttle_scope
    ...

class UploadView(APIView):
    throttle_scope = 'uploads'
    ...
```

</br>

settings.rest_framework配置修改
```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.ScopedRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'contacts': '1000/day',  # 这里和视图类中的throttle_scope保持一致，就能起到对视图类进行限流的目的
        'uploads': '20/day'
    }
}
```

# 排序
排序就是在对api进行请求的时候加上ordering参数，就可以在请求的返回结果中对某一个字段进行排序。  
比如：  
/books/bookinfos?ordering=title 就会在返回结果中针对title进行排序  

在DRF的排序需要依赖于django-filter实现，所以要先安装：  
`pip install django-filter`  

安装好之后要修改settings文件：  
```python
INSTALLED_APPS = [
    ...
    'django_filters',  # 需要在INSTALL_APPS中添加
]

# rest_framework中也要进行配置
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.OrderingFilter'
    ),
}
```  
最后还要在视图类显式地指定可以用于排序的字段,只有显式指定的字段才能用于排序。  

```python
class BookInfoModelViewSet(ModelViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer 
    ordering_fields = ('id', 'title') # 指定排序的字段，这样可以在请求中对这些字段进行排序
```

到这里就可以在API请求中对数据进行排序了，比如：  
/books/bookinfos?ordering=title  

# 过滤器
所谓过滤其实就是在API请求的时候加上一些参数，限制返回的结果，比如只查询id为1的书本信息，或者查询id大于2小于5的书本信息。  

DRF上应用过滤器有两种方式，一种配置简单，但是功能也有限，适用于比较需要简单的场景，另一种代码较多，但是功能强大。  

不论是那种方法，都需要依赖于django-filter，所以需要先安装：  
`pip install django-filter`  

安装好之后还要修改settings：  

```python
INSTALLED_APPS = [
    ...
    'django_filters',  # 需要在INSTALL_APPS中添加
]

# rest_framework中也要进行配置
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}
```

* **简单应用**  

过滤器的简单应用其实非常简单，只要在视图类中添加上filter_fields属性指定可以用于过滤的字段就可以了，如下：  

```python
class HeroInfoModelViewSet(ModelViewSet):
    queryset = HeroInfo.objects.all()
    serializer_class = HeroInfoSerializer
    ordering_fields = ['id', 'name']
    filter_fields = ['id', 'name']  # 指定可以用于过滤的字段
```

上面的代码中指明了可以对id和name进行过滤，比如： 
`GET /books/heroinfos?id=1`  
`GET /books/heroinfos?name=袁隆平`  

虽然这种方法很简单就能实现过滤的功能，但是也如上面的两个例子展示的那样，只能实现很简单的过滤，在过滤的时候必须明确地指定需要过滤的参数和对应的值，没办法搜索一个范围，比如我想搜索id大于2小于5之间所有的英雄就只能一次查询id=3,id=4，不能一次性查询。  
而且对于诸如时间这样的数据类型，这种简单的过滤器也只能按照字符串处理，而不能按照时间格式来处理。  

* **高级应用**

过滤器的高级应用需要配置多种数据类型的处理方式和自定义一个过滤器类。  

1. 在应用路径（book）下创建一个filters.py文件
filters.py里面主要包含两部分，一是各种数据类型的处理方式，比如布尔类型、字符串、时间等等，二是为视图类编写过滤器类，下面的代码中为BookInfoModelViewSet编写的过滤器类。

```python
from django_filters import rest_framework as filters
from . import models

BOOLEAN_LOOKUP = [
    'isnull',
    'exact',
    'in',
]

STRING_LOOKUP = [
    'iexact',
    'contains',
    'icontains',
    'startswith',
    'istartswith',
    'endswith',
    'iendswith',
    'regex',
    'iregex',
] + BOOLEAN_LOOKUP

NUMBER_LOOKUP = [
    'gt',
    'gte',
    'lt',
    'lte',
    'range',
] + BOOLEAN_LOOKUP

DATE_LOOKUP = [
    'year',
    'year__gt',
    'year__gte',
    'year__lt',
    'year__lte',
    'month',
    'month__gt',
    'month__gte',
    'month__lt',
    'month__lte',
    'day',
    'day__gt',
    'day__gte',
    'day__lt',
    'day__lte',
    'week',
    'week__gt',
    'week__gte',
    'week__lt',
    'week__lte',
    'week_day',
    'week_day__gt',
    'week_day__gte',
    'week_day__lt',
    'week_day__lte',
    'quarter',
    'quarter__gt',
    'quarter__gte',
    'quarter__lt',
    'quarter__lte',
] + NUMBER_LOOKUP

TIME_LOOKUP = [
    'hour',
    'hour__gt',
    'hour__gte',
    'hour__lt',
    'hour__lte',
    'minute',
    'minute__gt',
    'minute__gte',
    'minute__lt',
    'minute__lte',
    'second',
    'second__gt',
    'second__gte',
    'second__lt',
    'second__lte',
] + NUMBER_LOOKUP

DATETIME_LOOKUP = set([
    'date',
    'date__gt',
    'date__gte',
    'date__lt',
    'date__lte',
    'time',
    'time__gt',
    'time__gte',
    'time__lt',
    'time__lte',
] + DATE_LOOKUP + TIME_LOOKUP)

RESOLUTIONS = [
    'years',
    'months',
    'days',
    'hours',
    'minutes',
    'seconds',
]

TRUNC_DATETIME = [
    'year',
    'quarter',
    'month',
    'week',
    'day',
    'hour'
]


class BookInfoFilter(filters.FilterSet):
    '''
    为图书信息API配置过滤器
    '''
    class Meta:
        model = models.BookInfo  # 指定作用的数据库模型类
        # 指定需要为哪些字段设置过滤器
        fields = {
            'id': NUMBER_LOOKUP,
            'title': STRING_LOOKUP,
            'pub_date': DATE_LOOKUP,
            'read': NUMBER_LOOKUP,
            'is_delete': BOOLEAN_LOOKUP
        }
```

2. 在视图类中添加filter_class字段

```python
class BookInfoModelViewSet(ModelViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer
    ordering_fields = ('id', 'title')
    filter_class = BookInfoFilter  # 指定过滤器类
```

到这里就可以使用过滤器了。   
查询id大于10的书： `GET /books/bookinfos/?id__gte=10`  
查询出版年份早于1986年的书：  `GET /books/bookinfos/?pub_date__year__lt=1986`
查询书本名字以“天”开头的书：  `GET /books/bookinfos/?title__startswith=天`
过滤器的高级使用基本就是这样

# 分页
分页其实就是把数据库中的数据分批返回给请求者，而不是一次性把所有的数据都返回给请求者，这样容易出问题，比如数据库中商品表有一千万条数据，总不能一次性把者一千万条数据都返回给请求者，这样服务器要多大的配置才能完成，而且客户端也没办法接收这么多数据。  

应用分页有如下几个步骤：  
1. 创建自定义的分页处理器
文件位置如下：demo.utils.custom_pagination.py

```python
from rest_framework.pagination import PageNumberPagination as PNPG


class PageNumberPagination(PNPG):
    '''
    自定义分页类
    '''
    page_query_param = 'page'  # 前端查询某一页的参数名，如/books/bookinfos/?page=2
    page_size_query_param = 'page_size'  # 前端指定每一页返回的数据的条数，如/books/bookinfos/
    page_size = 5  # 后端默认设置的每页返回的数据的条数
    max_page_size = 5  # 前端允许的最大自定义每页的数据条数，也就是上面page_size的最大值
```

2. 修改settings文件

```python
# rest framework settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':  'demo.utils.custom_pagination.PageNumberPagination',
    'PAGE_SIZE': 100,  # 每页返回的数据调数，可以在分页处理器类中覆盖
}
```

3. 使用  
查询第二页内容： `GET /books/bookinfos/?page=2`
查询第二页，并且让每一页返回3条数据：  `GET /books/bookinfos/?page=2&page_size=3`

# 异常处理
DRF还有一个功能就是可以捕捉异常，默认情况下可以捕捉的异常如下：  
1. APIException 所有异常的父类
2. ParseError 解析错误
3. AuthenticationFailed 认证失败
4. NotAuthenticated 尚未认证
5. PermissionDenied 权限决绝
6. NotFound 未找到
7. MethodNotAllowed 请求方式不支持
8. NotAcceptable 要获取的数据格式不支持
9. Throttled 超过限流次数
10. ValidationError 校验失败

虽然能够捕捉的异常已经很多了，但是不可能捕捉所有的异常，这里以数据库异常为例。 

首先要创建自定义异常处理函数：  

```python
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
```   

然后还要修改settings文件：  

```python
# rest framework settings
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'demo.utils.custom_exception_handler.exception_handler',
}
```

这样就算可以了，如果想要验证的话，可以手动raise一个DatabaseError看看DRF能否捕捉到，这里没有准备案例。