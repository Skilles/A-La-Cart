import requests
import spoonacular
import logging

from gettingstarted.settings import spoon_api

MEAL_TYPES = {0: 'Breakfast', 1: 'Lunch', 2: 'Dinner'}


class Meal:

    def __init__(self, id, type:str, img_url, title, link):
        self.id = id
        self.img_url = img_url
        self.type = type
        self.title = title
        self.link = link




class SpoonUser:
    BASE_URL = 'https://api.spoonacular.com/'

    def __init__(self, profile):
        user = profile.user
        self.user_name = user.username
        self.email = user.email
        self.first_name = user.first_name
        self.last_name = user.last_name

        self.profile = profile
        self.connected = False
        self.json = None

        if not profile.user_name or not profile.hash:
            self.connect_user()
        else:
            self.connected = True
            self.hash = profile.hash
            self.user_name = profile.user_name

        self.api = spoon_api

    def connect_user(self):
        if self.connected:
            return

        url = self.BASE_URL + 'users/connect'
        response = requests.post(url, params=f'apiKey={spoon_api.api_key}', json={'username': self.user_name,
                                                                                  'firstName': self.first_name,
                                                                                  'lastName': self.last_name,
                                                                                  'email': self.email})
        if response.status_code == 200:
            self.json = json = response.json()
            self.user_name = json['username']
            self.password = json['spoonacularPassword']
            self.hash = json['hash']

            self.connected = True
        else:
            raise Exception("Exception when calling MealPlanningApi->connect_user\n" + response.text)

    def generate_recipes(self):
        response = self.api.generate_meal_plan(self.profile.get_diet(), self.profile.get_allergens(),
                                               self.profile.calories + ((self.profile.goal - 1) * 200), timeFrame='day')
        if response.status_code != 200:
            raise Exception("Exception when calling MealPlanningApi->generate_meal_plan")

        json = response.json()
        meals = json['meals']
        output = []
        for i in range(len(meals)):
            meal = meals[i]
            id = meal['id']
            title = meal['title']
            img_type = meal['imageType']
            img_url = f'https://spoonacular.com/recipeImages/{id}-240x150.{img_type}'
            link = meal['sourceUrl']
            j = i % 3
            output.append(Meal(id, MEAL_TYPES[j], img_url, title, link))
        return output

    def add_to_plan(self, meal: Meal):
        # Add meal to plan
        pass
    #     response = self.api.add_to_meal_plan({  "date": self.date,
    #                                             "slot": meal.type,
    #                                             "position": 0,
    #                                             "type": "RECIPES",
    #                                              "value": {
    #                                                         "id": meal.id,
    #                                                         "servings": 1,
    #                                                         "title": "meal.title",
    #                                                         "imageType": "meal.img_url",
    # }
    #                                                                 }
    #                                                                     )

    def add_meals_to_plan(self, ids):
        if len(ids) != 3:
            raise Exception(f"Not enough recipes! ({len(ids)})")
        for i in range(len(ids)):
            self.add_to_plan(Meal(ids[i], MEAL_TYPES[i]))
