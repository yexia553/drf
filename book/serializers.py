from django.db import models
from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import BookInfo, HeroInfo


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
    
    def validate(self, attrs):
        """
        参数验证函数，用于验证参数的合法性
        """
        if attrs['read'] < attrs['comment']:
            raise ValidationError("图书的阅读量应当大于等于评论量！")
        return attrs


class HeroInfoSerializer(serializers.ModelSerializer):
    """HeroInfo的序列化器"""
    class Meta:
        model = HeroInfo
        fields = '__all__'

    def validate(self, attrs):
        """
        参数验证函数，用于验证参数的合法性
        """
        return attrs


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

    def validate(self, attrs):
        """
        参数验证函数，用于验证参数的合法性
        """
        if attrs['read'] < attrs['comment']:
            raise ValidationError("图书的阅读量应当大于等于评论量！")
        return attrs

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


class HeroInfoBaseSerializers(serializers.Serializer):
    '''
    基于serializers.Serializer实现HeroInfo的序列化器，实际开发中使用的并不多
    '''
    GENDER_CHOICES = (
        (0, 'female'),
        (1, 'male')
    )
    id = serializers.IntegerField(label='ID', read_only=True)
    name = serializers.CharField(max_length=20, label='姓名')
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, label='性别', required=False)
    comment = serializers.CharField(max_length=200, label='描述信息')
    is_delete = serializers.BooleanField(default=False, label='逻辑删除标记')

    #### 当字段为外键时，有四种方法可以处理，如这里的book
    # 1. 添加read_only=True属性， 这样可以获取到对应book的id，但是只能用作序列化，不能对其进行反序列化
    # book = serializers.PrimaryKeyRelatedField(label='所属图书', read_only=True)
    # 2. 指定queryset，将在反序列化时被用于参数校验，得到的是对应的id
    # book = serializers.PrimaryKeyRelatedField(label='所属图书', queryset=BookInfo.objects.all())
    # 3. 设置为StringRelatedField，会返回模型类中__str__方法的返回值，得到的是一个字符串
    # book = serializers.StringRelatedField(label='所属图书')
    # 4. 使用关联对象的序列化器，得到的是OrderDict类型的关联对象的序列化器实例
    book = BookInfoBaseSerializer()

    def validate(self, attrs):
        """
        参数验证函数，用于验证参数的合法性
        """
        return attrs
    
    def create(self, validated_data):
        return HeroInfo.objects.create(validated_data)
    
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.name = validated_data.get('name', instance.name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.is_delete = validated_data.get('is_delete', instance.is_delete)
        instance.book = validated_data.get('book', instance.book)
        instance.save()
        return instance
    