from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . import models
from profile_user.models import ProfileUser
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
        slug = product.slug
        image = product.image

        if image:
            image = image.url
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
        http_referer = request.META.get(
            'HTTP_REFERER', reverse('product:list'))
        variation_id = request.GET.get('vid')

        cart = request.session.get('cart')

        if not variation_id:
            return redirect(http_referer)

        if not cart:
            return redirect(http_referer)

        if variation_id in cart:
            del cart[variation_id]

        request.session.save()
        messages.success(request, 'Produto removido do carrinho')
        return redirect(http_referer)


class Cart(View):
    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart', {})
        context = {
            'cart': cart
        }
        return render(request, 'product/cart.html', context)


class PurchaseSummary(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('profile:create')

        profile = ProfileUser.objects.filter(user=self.request.user).exists()

        if not profile:
            messages.error(
                self.request, 
                'Você precisa criar um perfil para realizar a compra'
            )

            return redirect('profile:create')

        if not self.request.session.get('cart'):
            messages.error(self.request, 'Seu carrinho está vazio')
            return redirect('product:list')

        context = {
            'user': self.request.user,
            'cart': self.request.session.get('cart', {})
        }
        return render(self.request, 'product/purchasesummary.html', context)
