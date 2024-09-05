from django.db import models
from random import randint

class RandomNumber(models.Model):
    number = models.IntegerField()

    @classmethod
    def generate_numbers(cls, count=5, min_value=1, max_value=10):
        cls.objects.all().delete()  # Удаляем все существующие записи
        for _ in range(count):
            cls.objects.create(number=randint(min_value, max_value))


class BracketsRandomNumber(RandomNumber):

    @classmethod
    def generate_numbers(cls, count=5, min_value=1, max_value=10):
        super().generate_numbers(count, min_value, max_value)


class NeighboursRandomNumber(RandomNumber):

    @classmethod
    def generate_numbers(cls, count=1, min_value=0, max_value=36):
        return super().generate_numbers(count, min_value, max_value)
    

class BjRandomNumber(RandomNumber):

    @classmethod
    def generate_numbers(cls, count=1, min_value=1, max_value=100):
        return super().generate_numbers(count, min_value, max_value)


class VoisinsDeZero(RandomNumber):

    @classmethod
    def generate_numbers(cls, count=1, min_value=9, max_value=1700):
        return super().generate_numbers(count, min_value, max_value)


class Tier(RandomNumber):

    @classmethod
    def generate_numbers(cls, count=1, min_value=6, max_value=1200):
        return super().generate_numbers(count, min_value, max_value)


class Orphelins(RandomNumber):

    @classmethod
    def generate_numbers(cls, count=1, min_value=5, max_value=900):
        return super().generate_numbers(count, min_value, max_value)


class ZeroSpiel(RandomNumber):

    @classmethod
    def generate_numbers(cls, count=1, min_value=4, max_value=700):
        return super().generate_numbers(count, min_value, max_value)
