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
    简单应用（笔记）
    模板应用（AND）
# 分页
# 异常处理