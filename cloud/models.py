from django.db import models

# Create your models here.
class User(models.Model):
    #campos del usuario
    name = models.CharField(max_length=15,unique=True)
    password = models.CharField(max_length=10)
    email = models.CharField(max_length=35)
    
class Directory(models.Model):
    #campos del directorio
    name = models.CharField(max_length=20,primary_key=True)
    hierarchy = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class File(models.Model):
    #campos del directorio
    name = models.CharField(max_length=50,primary_key=True)
    size = models.IntegerField()
    date = models.DateField()
    path = models.TextField()
    dir = models.ForeignKey(Directory,on_delete=models.CASCADE)