from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()


class TestModelAllTypes(models.Model):
    field_binary = models.BinaryField()
    field_boolean = models.BooleanField()
    # field_null_boolean = models.NullBooleanField() deprecated
    field_null_boolean = models.BooleanField(null=True)
    field_date = models.DateField()
    field_time = models.TimeField()
    field_datetime = models.DateTimeField()
    field_duration = models.DurationField()
    # field_auto_aka_id = models.AutoField()
    field_big_integer = models.BigIntegerField()
    field_decimal = models.DecimalField(decimal_places=10, max_digits=12)
    field_float = models.FloatField()
    field_integer = models.IntegerField()
    field_positive_integer = models.PositiveIntegerField()
    field_positive_small_integer = models.PositiveSmallIntegerField()
    field_small_integer = models.SmallIntegerField()
    field_char = models.CharField(max_length=10)
    field_text = models.TextField()
    field_email = models.EmailField()
    field_file = models.FileField()
    field_file_path = models.FilePathField()
    field_image = models.ImageField()
    field_generic_ip_address = models.GenericIPAddressField()
    field_slug = models.SlugField()
    field_url = models.URLField()
    field_uuid = models.UUIDField()


class Company(models.Model):
    name = models.CharField(max_length=50)


class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
