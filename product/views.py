from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . import models
from pprint import pprint


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
        # TODO: Remover essas linhas comentadas
        # if request.session.get('cart'):
        #     del request.session['cart']
        #     request.session.save()

        http_referer = request.META.get(
            'HTTP_REFERER', reverse('product:list'))
        variation_id = request.GET.get('vid')

        if not variation_id:
            messages.error(request, 'Produto não existe')
            return redirect(http_referer)

        variation = get_object_or_404(models.Variation, id=variation_id)
        variation_inventory = variation.inventory
        product = variation.product

        product_id = product.id
        product_name = product.name
        variation_name = variation.name or ''
        unit_price = variation.price
        promotional_unit_price = variation.promotional_price
        quantity = 1
        slug = product.slug
        image = product.image

        if image:
            image = image.name
        else:
            image = ''

        if variation.inventory < 1:
            messages.error(request, 'Estoque insuficiente')
            return redirect(http_referer)

        if not request.session.get('cart'):
            request.session['cart'] = {}
            request.session.save()

        cart = request.session['cart']

        if variation_id in cart:
            quantity_cart = cart[variation_id]['quantity']
            quantity_cart += 1

            if variation_inventory < quantity_cart:
                messages.warning(
                    request,
                    f'Estoque insuficiente para {quantity_cart}x no '
                    f'produto "{product_name}". Adicionamos {variation_inventory}x '
                    f'no seu carrinho.'
                )
                quantity_cart = variation_inventory

            cart[variation_id]['quantity'] = quantity_cart
            cart[variation_id]['quantitative_price'] = unit_price * quantity_cart
            cart[variation_id]['promotional_quantitative_price'] = promotional_unit_price * quantity_cart

        else:
            cart[variation_id] = {
                'product_id': product_id,
                'product_name': product_name,
                'variation_name': variation_name,
                'variation_id': variation_id,
                'unit_price': unit_price,
                'promotional_unit_price': promotional_unit_price,
                'quantitative_price': unit_price,
                'promotional_quantitative_price': promotional_unit_price,
                'quantity': 1,
                'slug': slug,
                'image': image
            }

        request.session.save()
        messages.success(
            request, 
            f'Produto "{product_name.upper()}"-"{variation_name.upper()}" adicionado ao '
            f'carrinho {cart[variation_id]["quantity"]}x'
        )
        return redirect(http_referer)


class RemoveFromCartProduct(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Remove From Cart Product')


class Cart(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'product/cart.html')


class Finish(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Finish')
