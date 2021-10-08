from django.db import models


class BookInfo(models.Model):
    title = models.CharField(max_length=20, verbose_name='书名', help_text='书名')
    pub_date = models.DateField(verbose_name='发布日期')
    read = models.IntegerField(default=0, verbose_name='阅读量')
    comment = models.IntegerField(default=0, verbose_name='评论量')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除标记')
    image = models.ImageField(verbose_name='图书', upload_to='book', null=True, blank=True)
    
    class Meta:
        db_table = 'books'
        verbose_name = '图书'
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return self.title


class HeroInfo(models.Model):
    GENDER_CHOICES = (
        (0, 'female'),
        (1, 'male')
    )

    name = models.CharField(max_length=20, verbose_name='姓名')
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0, verbose_name='性别')
    comment = models.CharField(max_length=200, verbose_name='描述信息')
    book = models.ForeignKey(BookInfo, on_delete=models.CASCADE, verbose_name='所属图书')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除标记')

    class Meta:
        db_table = 'heros'
        verbose_name = '英雄'
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return self.name