from django.db import models

# Create your models here.
class UserDetails(models.Model):
	Username = models.CharField(max_length = 100,default = None)
	Password = models.CharField(max_length = 100,default = None)
	EmailID = models.CharField(max_length = 100,default = None)

	class Meta:
		db_table = 'UserDetails'