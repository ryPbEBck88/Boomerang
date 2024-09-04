
from django.db import models
from random import randint

class RandomNumber(models.Model):
    number = models.IntegerField()

    @classmethod
    def generate_numbers(cls, count=5, min_value=1, max_value=10):
        cls.objects.all().delete()  # Удаляем все существующие записи
        for _ in range(count):
            cls.objects.create(number=randint(min_value, max_value))
