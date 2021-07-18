from django.db import models

# Create your models here.

##用户注册
class GeneralUser(models.Model):
    gender = [
        ("m", "男"),
        ("f", "女")
    ]

    name = models.CharField(max_length=50, verbose_name="姓名")
    gender = models.CharField(max_length=10, choices=gender, default='m', verbose_name="性别")
    birthday = models.DateField(verbose_name="生日")
    email = models.EmailField(verbose_name="邮箱")
    info = models.CharField(max_length=255, verbose_name="个人简介", help_text="一句话介绍自己，不要超过250字")

    no = models.CharField(max_length=4, verbose_name="注册编号")
    number = models.CharField(max_length=6, verbose_name="用户编号")
    password = models.CharField(max_length=30, verbose_name="密码")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['no', 'number'], name='generaluser_id'),
        ]

    def get_id(self):
        return self.no + self.number

    def __str__(self):
        return "%s (%s)" % (self.no + self.number, self.name)

##管理者注册
class Admin(models.Model):
    genders = [
        ("m", "男"),
        ("f", "女")
    ]

    name = models.CharField(max_length=50, verbose_name="姓名")
    gender = models.CharField(max_length=10, choices=genders, default='m', verbose_name="性别")
    birthday = models.DateField(verbose_name="生日")
    email = models.EmailField(verbose_name="邮箱")
    info = models.CharField(max_length=255, verbose_name="个人简介", help_text="不要超过250字")

    no = models.CharField(max_length=3, verbose_name="注册编号")
    number = models.CharField(max_length=7, verbose_name="管理员编号")
    password = models.CharField(max_length=30, verbose_name="密码")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['no', 'number'], name='admin_id'),
        ]

    def get_id(self):
        return self.no + self.number

    def __str__(self):
        return "%s (%s)" % (self.no + self.number, self.name)