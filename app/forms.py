from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.postgres.forms import SimpleArrayField

from .api.spoon_api import SpoonUser
from .models import Profile
from .util import calculate_calories

import logging


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    # fields we want to include and customize in our form
    weight = forms.IntegerField(max_value=1000,
                                min_value=0,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'weight',
                                                              'class': 'form-control',
                                                              }))
    height = forms.IntegerField(required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'height',
                                                              'class': 'form-control',
                                                              }))
    sex = forms.ChoiceField(choices=[("M", "Male"), ("F", "Female")],
                            required=True,
                            widget=forms.Select(attrs={'placeholder': 'sex',
                                                       'class': 'form-control',
                                                       }))
    age = forms.IntegerField(max_value=150,
                             min_value=10,
                             required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'age',
                                                           'class': 'form-control',
                                                           }))
    diet = forms.ChoiceField(choices=Profile.DIET_CHOICES,
                             required=True,
                             widget=forms.Select(attrs={'placeholder': 'diet',
                                                        'class': 'form-control',
                                                        }))
    allergens = forms.MultipleChoiceField(choices=Profile.ALLERGENS_CHOICES,
                                          required=False,
                                          widget=forms.CheckboxSelectMultiple(attrs={'placeholder': 'allergens',
                                                                                     'class': 'form-control',
                                                                                     }))
    goal = forms.ChoiceField(choices=[(0, "Lose Weight"), (1, "Maintain Weight"), (2, "Gain Weight")],
                             required=True,
                             widget=forms.Select(attrs={'placeholder': 'goal',
                                                        'class': 'form-control',
                                                        }))

    def save(self, commit=True):
        instance = super(UpdateProfileForm, self).save(commit=False)
        if instance.calories == -1:
            print(f"Setting calories for user ID {instance.user_id}")
            logging.info(f"Setting calories for user ID {instance.user_id}")
            instance.calories = calculate_calories(self.cleaned_data['weight'], self.cleaned_data['height'],
                                                   self.cleaned_data['age'], self.cleaned_data['sex'])
            # Initialize fields for the API if they are not found
            if instance.user_name == '' or instance.hash == '':
                spoon_user = SpoonUser(instance)
                instance.user_name = spoon_user.user_name
                instance.hash = spoon_user.hash

            if commit:
                instance.save()
        return instance

    class Meta:
        model = Profile
        fields = ['diet', 'goal', 'allergens']
        exclude = ('calories', 'user_name', 'hash')


class RecommendForm(forms.Form):
    ids = SimpleArrayField(forms.IntegerField(), required=True)


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class RegisterForm(UserCreationForm):
    # fields we want to include and customize in our form
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
