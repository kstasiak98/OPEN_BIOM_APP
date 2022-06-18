from django.db import models


# Create your models here.


# def user_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
#     return 'user_{0}/{1}'.format(instance.user.id, filename)


class CustomerImage(models.Model):
    image_name = models.CharField(max_length=200)
    image_field = models.ImageField(upload_to='uploads/')

    def __str__(self):
        return self.image_name


class TestImage(models.Model):
    image_name = models.CharField(max_length=200, default="test")
    image_field = models.ImageField(upload_to='uploads/')

    def __str__(self):
        return self.image_name


class Image_Test(models.Model):
    image = models.ImageField(upload_to='test/')

    def __str__(self):
        return "TEST"



