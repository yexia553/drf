from rest_framework import serializers
from .models import BookInfo


class BookInfoSerializer(serializers.ModelSerializer):
    """定义序列化器"""
    class Meta:
        model = BookInfo  # 指定作用的模型
        fields = '__all__'  # 指定序列化的字段，这里让所有字段都能被序列化