from django.db import models


class Organization(model.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    email_contact = models.CharField(max_length=30)
    phone_contact = models.CharField(max_length=30)
