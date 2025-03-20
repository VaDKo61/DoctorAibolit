from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Schedule(models.Model):
    name_medicine = models.CharField(max_length=150)
    periodicity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(15)])
    duration = models.CharField(max_length=50)
    user_id = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])