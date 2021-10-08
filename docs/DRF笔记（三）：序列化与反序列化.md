**笔记中提到的代码repo：https://github.com/yexia553/drf**

# 序列化与反序列化
简单地说，序列化就是从数据库中取出数据处理后传给API（请求方）；反序列化就是从API（请求方）获取数据处理后存到数据库中。

# Serializer类
在DRF框架中，序列化与反序列化是通过Serializer来实现的，常用的有serializer.ModelSerializer和serializer.Serializer这两个类，前者是后者的子类。  
下面分别说一下这两个类。  

**1.ModelSerialzer**
在前一篇[DRF笔记（二）：DRF框架初体验 ](http://www.panzhixiang.cn/article/2021/9/9/43.html)中使用的其实就是ModelSerializer，在实际开发中使用的比较多的也是这个类。
可以参见代码仓库中book.serializers中的BookInfoSerializer和HeroInfoSerializer这两个类。
BookInfoSerializer代码如下： 

```python
class BookInfoSerializer(serializers.ModelSerializer):
    """定义序列化器"""

    # 如果想在“一对多”的“一”中关联“多”，就要指定many=True这个参数
    # 比如这里要查询出属于本书的所有英雄人物的信息，字段名必须是 关联模型名+'_set'这种格式，如“heroinfo_set”
    heroinfo_set = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = BookInfo  # 指定作用的模型
        fields = '__all__'  # 指定序列化的字段，这里让所有字段都能被序列化
        # fields = ['id', 'title', 'pub_date']  # 指定期望可以序列化的字段
        # exclude = ['image']  # 除了image字段，其他字段都包含
        # read_only_fields = ['id']  # 指定只读字段
        # extra_kwagrs 可用于修改或添加原有的参数
        extra_kwargs = {
            'read': {'min_value': 0, 'required': True},
            'comment': {'min_value': 0, 'required': True},
        }
```
BookInfoSerialzer对的Django Model是book.models.BookInfo，其主要代码都在Meta中，必将常用的几个选项我都在代码中做了详细的解释，可以参考。

**2.Serializer**
serializer.Serializer 这个类就没有上面的那么方便了，很多东西都要自己定义，详细代码可以参见代码仓库中的book.serializers.BookInfoBaseSerializer和book.serializers.HeroBaseSerializers这两个类，其中book.serizlizers.BookInfoBaseSerializer的代码如下：  

```python
class BookInfoBaseSerializer(serializers.Serializer):
    """
    相对于ModelSerializer类，Serializer需要写更多的代码，
    但是当需要序列化的内容没有对应的Django Model的时候这种方式更适合
    """
    # read_only属性表示这个字段只能用于序列化，也就是只能从数据库中读取然后给api，
    # 但是不能通过api获取数据对它进行更新，比如id
    id = serializers.IntegerField(label='ID', read_only=True)
    # required属性表示api传递数据过来的时候这个字段是不是必须的，
    # 一般在Django的Model没有默认值的时候都是必须的，否则会报错
    title = serializers.CharField(max_length=20, label='书名', required=True)  
    pub_date = serializers.DateField(label='发布日期', required=True)
    read = serializers.IntegerField(label='阅读量', required=False)
    comment = serializers.IntegerField(label='评论量', required=False)
    is_delete = serializers.BooleanField(label='逻辑删除标记', required=False)
    image = serializers.ImageField(label='图书', required=False)
    # 如果想在“一对多”的“一”中关联“多”，就要指定many=True这个参数
    # 比如这里要查询出属于本书的所有英雄人物的信息，字段名必须是 关联模型名+'_set'这种格式，如“heroinfo_set”
    heroinfo_set = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    def create(self, validated_data):
        """
        创建一条记录，可以直接调用Django Model中create方法创建
        """
        return BookInfo.objects.create(validated_data)
    
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.title = validated_data.get('title', instance.title)
        instance.pub_date = validated_data.get('pub_date', instance.pub_date)
        instance.read = validated_data.get('read', instance.read)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.is_delete = validated_data.get('is_delete', instance.is_delete)
        instance.heroinfo_set = validated_data.get('heroinfo_set', instance.heroinfo_set)
        instance.save()
        return instance
```
可以看到，代码比使用ModelSerializer多了很多，需要自己定义每个字段；更重要的是还要自己定义create和update这两个方法，create用于创建新的记录，update用于修改数据库中已有的记录。

**3.ModelSerializer和Serializer的取舍**
通过上面两段代码来看，ModelSerializer明显优于Serializer，但也不是说就永远使用ModelSerializer。  
一般来说，如果是为Django的模型类写序列化器就选择ModelsSerializer，因为它帮我们做了很多事情，需要写的代码比较少；如果后端没有对应的模型类，那么就只能选择Serializer。  

# 校验
前面提到反序列化是从API获取数据，处理后存到数据库中。这里说的“处理”其中有一个环节就是对获取到的数据进行校验，校验合格后才能真正存储到数据库中。  

**1.编写校验函数**
在DRF框架中有多种方法可以编写校验函数，这里只写一种比较通用的示例。  
假设我们要多BookInfo序列化器做一个校验，要求图书的阅读量大于等于评论量，否则报错，校验函数如下：  

```python
def validate(self, attrs):
    """
    参数验证函数，用于验证参数的合法性，函数名是固定的，就叫做validate；
    attrs是从API获取的参数；
    最后一定要返回attrs，这里返回的attrs就是validated_data否则就会丢失数据，
    """
    if attrs['read'] < attrs['comment']:
        raise ValidationError("图书的阅读量应当大于等于评论量！")
    return attrs
```

**2.如何使用校验函数**
看代码和注释：  

```python
from book.serializers import BookInfoSerializer
from book.models import BookInfo

book = BookInfo.obejcts.get(pk=1)
s = BookInfoSerializer(data=book)  # 将Django的模型对象（book）传给序列化器的data参数
s.is_valid()  # 进行校验,is_valid方法就会调用我们定义的validate函数，如果返回值为True，说明校验通过，否则校验失败
s.errors  # 如果校验失败可以查看errors属性来获取具体报错内容
s.validated_data  # 如果校验通过，可以通过validated_data来或者检验后的数据，也就是validate函数中最后返回的attrs
```
is_valid方法还可以传入一个raise_exception=True参数，如果校验失败会直接给API返回一个HTTP 400 Bad Request的响应。  
