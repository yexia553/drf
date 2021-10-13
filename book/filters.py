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