from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse
from django.views.generic.base import TemplateResponseMixin
from . import models


class ListProduct(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 3


class DetailsProduct(DetailView):
    model = models.Product
    template_name = 'product/details.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


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
