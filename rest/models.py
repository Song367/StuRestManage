from django.db import models


class Canteen(models.Model):
    CID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16, verbose_name="食堂名", unique=True)
    stu = models.ManyToManyField("Login", null=True)
    secret = models.CharField(max_length=128,null=False,unique=True)
    canteen_store = models.ManyToManyField("Store",  null=True)


class Login(models.Model):
    LID = models.CharField(primary_key=True, max_length=64, verbose_name="登录ID")
    username = models.CharField(max_length=32)


class Store(models.Model):
    SID = models.AutoField(primary_key=True)
    StoreName = models.CharField(max_length=32, verbose_name="店铺名")
    food = models.ManyToManyField("FoodList", null=True)


class FoodList(models.Model):
    FID = models.BigAutoField(primary_key=True)
    FName = models.CharField(max_length=32, verbose_name="菜名")
    Price = models.CharField(max_length=16, verbose_name="价格")
    Image = models.FileField(max_length=128, verbose_name="菜图片", upload_to='img')
