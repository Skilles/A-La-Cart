from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from .api.spoon_api import SpoonUser
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm, RecommendForm
import logging

from .models import Profile


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})


class CreateProfileView(LoginRequiredMixin, View):
    form_class = UpdateProfileForm
    initial = {'key': 'value'}
    template_name = 'create_profile.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user.profile)

        if form.is_valid():
            form.save(request.user.id)
            username = request.user.username
            print(form.cleaned_data.items())
            messages.success(request, f'Profile updated for {username}')

            return redirect(to='/')

        return render(request, self.template_name, {'form': form})

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the update profile when not logged in
        if not request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(CreateProfileView, self).dispatch(request, *args, **kwargs)


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class RecommendView(LoginRequiredMixin, View):
    form_class = RecommendForm
    template_name = 'recommend.html'

    def get(self, request, *args, **kwargs):
        spoon_user = SpoonUser(request.user.profile)
        recipes = spoon_user.generate_recipes()

        ids = [str(recipe.id) for recipe in recipes]
        ids = ','.join(ids)
        initial = {'ids': ids}
        form = self.form_class(initial=initial)
        return render(request, self.template_name, {'recipes': recipes})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            ids = list(form.cleaned_data.get('ids'))

            spoon_user = SpoonUser(request.user.profile)
            spoon_user.add_meals_to_plan(ids)

            messages.success(request, 'Your plan has been updated')
            return redirect(to='grocery')
        else:
            messages.error(request, 'ERROR: Not enough recipes selected')
            return redirect(to='recommend')


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            logging.info(form.cleaned_data.items())
            messages.success(request, f'Account created for {username}')

            return redirect(to='/')

        return render(request, self.template_name, {'form': form})

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('index')


def about(request):
    return render(request, "about.html")


# @login_required
# def recommend(request):
#     if request.method == 'POST':
#         recipe_id = request.POST.get('recipe_id')
#         spoon_user = SpoonUser(request.profile)
#         spoon_user.add_to_plan(recipe_id)
#
#     return render(request, "recommend.html")


# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def db(request):
    # Display every product in the database
    # products = Product.objects.all()
    return render(request, "db.html", {'products': None})
