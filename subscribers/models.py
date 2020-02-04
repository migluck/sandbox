from django.db import models

# Create your models here.
class Subscriber(models.Model):
    """Model class to hold subscribers"""
    
    email = models.CharField(max_length=100, blank=False, help_text='Email address')
    full_name = models.CharField(max_length=100, blank=False, null=False, help_text="First and Last name")
    
    def __str__(self):
        """String representation of object"""
        return self.full_name
    
    class Meta: # noqa
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscribers"
        