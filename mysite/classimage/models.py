from django.db import models

# Create your models here.
class Face(models.Model):
    name = models.CharField(max_length=50)
    face_Main_Img = models.ImageField(upload_to='images/')