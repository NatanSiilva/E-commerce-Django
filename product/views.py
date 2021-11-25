from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse


class ListProduct(ListView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('List Product')


class DetailsProduct(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Details Product')


class AddToCartProduct(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Add To Cart Product')


class RemoveFromCartProduct(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Remove From Cart Product')


class Cart(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Cart')


class Finish(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Finish')
