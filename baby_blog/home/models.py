from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from django.urls import reverse
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(upload_to = 'profile/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} profile"    
    
    @property
    def imageURL(self):
        try: 
            url = self.image.url
        except:
            url = '/images/profile/default.png'
        return url 
        # /images/ = media_url


    # def save(self, *args, **kwargs):
    #     super(Profile, self).save(*args, **kwargs)

    #     img = Image.open(self.image.path)

    #     if img.height > 300 or img.width > 300:
    #         output_size = (300,300)
    #         img.thumbnail(output_size)

    #         img.save(self.image.path)
        
    #     else:
    #         img.close()

    # def save(self, *args, **kwargs):

    #     if self.pk:
    #         old_profile = Profile.objects.get(pk=self.pk)
    #         old_image = old_profile.image if old_profile.image else None
    #     else:
    #         old_image = None
        
    #     super(Profile, self).save(*args, **kwargs)

    #     # when uploaded, delete the old one
    #     if self.image and self.image != old_image:
    #         if old_image:
    #             try:
    #                 # Delete the old image from the filesystem
    #                 if os.path.isfile(old_image.path):
    #                     os.remove(old_image.path)
    #             except Exception as e:
    #                 print(f"Error deleting old image: {e}")

    #     # delete current, when it's deleted
    #     elif not self.image and old_image:
    #         try:
    #             if os.path.isfile(old_image.path):
    #                 os.remove(old_image.path)
    #         except Exception as e:
    #             print(f"Error deleting current image: {e}")

    #     if self.image:
    #         img = Image.open(self.image.path)
    #         if img.height > 300 or img.width > 300:
    #             output_size = (300, 300)
    #             img.thumbnail(output_size)
    #             img.save(self.image.path)
    #         img.close()



class Posts(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title}"
    
    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'pk':self.pk})