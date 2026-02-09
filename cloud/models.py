from django.db import models

# Create your models here.
class User(models.Model):
    #campos del usuario
    name = models.CharField(max_length=15,unique=True)
    password = models.CharField(max_length=10)
    email = models.CharField(max_length=35)
    
class Directory(models.Model):
    #campos del directorio
    name = models.CharField(max_length=20)
    hierarchy = models.TextField()
    level = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class File(models.Model):
    #campos del directorio
    name = models.CharField(max_length=50)
    size = models.IntegerField()
    date = models.DateField()
    dir = models.ForeignKey(Directory,on_delete=models.CASCADE)