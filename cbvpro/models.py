from django.db import models

# Create your models here.
class UserInfo(models.Model):

    user_type_choices = (
        (1,'normal'),
        (2,'vip')
    )
    user_type = models.IntegerField(choices=user_type_choices)
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=50)
    # 隶属于UserGroup
    group = models.ForeignKey('UserGroup',on_delete=models.CASCADE)

    def __str__(self):
        return self.username

class UserToken(models.Model):
    user = models.OneToOneField('UserInfo', on_delete=models.CASCADE)
    token = models.CharField(max_length=50)

class UserGroup(models.Model):

    def __str__(self):
        return self.title

    title = models.CharField(max_length=50)

class Role(models.Model):

    def __str__(self):
        return self.title

    title = models.CharField(max_length=50)