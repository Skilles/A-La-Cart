from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile

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
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']

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


class QuizForm(forms.Form):
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
    sex = forms.ChoiceField(choices=("Male", "Female"),
                            required=True,
                            widget=forms.RadioSelect(attrs={'placeholder': 'sex',
                                                            'class': 'form-control',
                                                            }))
    age = forms.IntegerField(max_value=150,
                             min_value=10,
                             required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'age',
                                                           'class': 'form-control',
                                                           }))
    diet = forms.TypedMultipleChoiceField(choices=(
    "Vegetarian", "Vegan", "Pescetarian", "Paleo", "Ovo-Vegetarian", "Ovo-Vegan", "Ovo-Pescetarian", "Ovo-Paleo"),
                                          required=True,
                                          widget=forms.SelectMultiple(attrs={'placeholder': 'diet',
                                                                             'class': 'form-control',
                                                                             }))
    goal = forms.MultipleChoiceField(choices=("Lose Weight", "Gain Weight", "Maintain Weight"),
                                     required=True,
                                     widget=forms.SelectMultiple(attrs={'placeholder': 'goal',
                                                                        'class': 'form-control',
                                                                        }))

    class Meta:
        model = User
        fields = ['weight', 'height', 'sex', 'age']
