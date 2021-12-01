from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from . import models
from . import forms
import copy


class BaseProfile(View):
    template_name = 'profile/create.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.cart = copy.deepcopy(self.request.session.get('cart', {}))

        self.profile = None

        if self.request.user.is_authenticated:
            self.profile = models.ProfileUser.objects.filter(
                user=self.request.user
            ).first()

            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    user=self.request.user,
                    instance=self.request.user
                ),
                'profileform': forms.ProfileForm(
                    data=self.request.POST or None,
                    instance=self.profile
                ),
            }
        else:
            self.context = {
                'userform': forms.UserForm(data=self.request.POST or None),
                'profileform': forms.ProfileForm(data=self.request.POST or None),
            }

        self.userform = self.context['userform']
        self.profileform = self.context['profileform']

        if self.request.user.is_authenticated:
            self.template_name = 'profile/update.html'

        self.render = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        return self.render


class CreateProfile(BaseProfile):
    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.profileform.is_valid():
            return self.render

        username = self.userform.cleaned_data.get('username')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')
        password = self.userform.cleaned_data.get('password')

        if self.request.user.is_authenticated:
            user = get_object_or_404(User, username=self.request.user.username)

            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name

            if password:
                user.set_password(password)

            user.save()

            if not self.profile:
                self.profileform.cleaned_data['user'] = user
                profile = models.ProfileUser(**self.profileform.cleaned_data)
                profile.save()
            else:
                profile = self.profileform.save(commit=False)
                profile.user = user
                profile.save()
        else:
            user = self.userform.save(commit=False)
            user.set_password(password)
            user.save()

            profile = self.profileform.save(commit=False)
            profile.user = user
            profile.save()

        if password:
            authenticated_user = authenticate(
                self.request, username=user, password=password
            )

            if authenticated_user:
                login(self.request, user)

        self.request.session['cart'] = self.cart
        self.request.session.save()

        messages.success(
            self.request, 'Seu cadastro foi realizado com sucesso!'
        )

        messages.success(
            self.request, 'Login realizado com sucesso!'
        )

        return redirect('profile:create')


class UpdateProfile(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Update Profile')


class Login(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            messages.error(self.request, 'Preencha todos os campos')
            return redirect('profile:create')

        authenticated_user = authenticate(
            self.request, username=username, password=password
        )

        if not authenticated_user:
            messages.error(
                self.request, 'Usuário ou senha inválidos!'
            )

        login(self.request, authenticated_user)

        messages.success(self.request, 'Login realizado com sucesso!')

        return redirect('product:cart')


class Logout(View):
    def get(self, *args, **kwargs):
        cart = copy.deepcopy(self.request.session.get('cart', {}))

        logout(self.request)

        self.request.session['cart'] = cart
        self.request.session.save()

        return redirect('product:list')
