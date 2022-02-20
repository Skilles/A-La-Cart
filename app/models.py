import logging

from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from multiselectfield import MultiSelectField


# Create your models here.
# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    DIET_CHOICES = [
        (0, "Vegetarian"), (1, "Vegan"), (2, "Pescetarian"), (3, "Paleo"), (4, "Ovo-Vegetarian"),
        (5, "Ovo-Vegan"), (6, "Ovo-Pescetarian"), (7, "Ovo-Paleo")]
    ALLERGENS_CHOICES = [(0, "Gluten"), (1, "Dairy"), (2, "Eggs"), (3, "Fish"), (4, "Peanuts")]

    # weight = models.IntegerField(default=0, max_length=3)
    # height = models.IntegerField(default=0, max_length=3)
    # sex = models.BooleanField()
    # age = models.IntegerField(default=0, max_length=3)
    calories = models.IntegerField(default=-1)
    # Use the indicies to store diet and goal
    diet = models.IntegerField(default=-1)
    allergens = MultiSelectField(choices=ALLERGENS_CHOICES, default="")
    goal = models.IntegerField(default=-1)

    # Api related fields
    user_name = models.CharField(max_length=100, default="")
    hash = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.user.username

    def get_diet(self):
        return self.DIET_CHOICES[self.diet][1]

    def get_allergens(self):
        if not self.allergens or self.allergens == '':
            return ''
        keys = str(self.allergens).split(",")
        logging.info(keys)
        allergens = []
        for key in keys:
            allergens.append(self.ALLERGENS_CHOICES[int(key)][1])
        return ', '.join(allergens)

    # resizing images
    # def save(self, *args, **kwargs):
    #     super().save()
    #
    #     img = Image.open(self.avatar.path)
    #
    #     if img.height > 100 or img.width > 100:
    #         new_img = (100, 100)
    #         img.thumbnail(new_img)
    #         img.save(self.avatar.path)
