from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
from django.views.generic.base import TemplateResponseMixin
from . import models


class ListProduct(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 3


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
