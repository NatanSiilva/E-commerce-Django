from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse


class CreateProfile(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Create Profile')


class UpdateProfile(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Update Profile')


class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Login')


class Logout(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Logout')
