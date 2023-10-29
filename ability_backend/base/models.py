from django.db import models

class Login(models.Model):  # Model class names are typically capitalized.
    id = models.AutoField(primary_key=True)  # Use AutoField for primary keys.
    username = models.CharField(max_length=255)  # Use CharField for text fields.
    password = models.CharField(max_length=255)  # Use CharField for text fields.
    role = models.CharField(max_length=255)
    is_deleted = models.IntegerField(default=0)  # Use IntegerField for integers.

    class Meta:
        app_label = 'base'
