from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView
from django.views import View
from django.contrib import messages
from django.http import HttpResponse
from product.models import Product, Variation
from utils import utils
from .models import Order, OrderItem


class DispatchLoginRequiredMixin(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('profile:create')

        return super().dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        qs = qs.filter(user=self.request.user)

        return qs


class Pay(DispatchLoginRequiredMixin, DetailView):
    model = Order

    template_name = 'order/pay.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'order'


class SaveOrder(View):
    template_name = 'order/pay.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Login nescessary')
            return redirect('profile:create')

        if not self.request.session.get('cart'):
            messages.error(self.request, 'Cart is empty')
            return redirect('product:list')

        cart = self.request.session.get('cart')
        cart_variatioins = [v for v in cart]

        variations_db = list(
            Variation.objects.select_related('product')
            .filter(id__in=cart_variatioins)
        )

        for variations in variations_db:
            vid = str(variations.id)

            inventory = variations.inventory
            cart_qtd = cart[vid]['quantity']
            unit_price = cart[vid]['unit_price']
            promotional_unit_price = cart[vid]['promotional_unit_price']

            error_msg_inventory = ''

            if inventory < cart_qtd:
                cart[vid]['quantity'] = inventory
                cart[vid]['quantitative_price'] = inventory * unit_price
                cart[vid]['promotional_quantitative_price'] = inventory * \
                    promotional_unit_price

                error_msg_inventory = 'Estoques insuficientes para alguns produtos do seu carrinho. '\
                    'Reduzimos a quantidade desses produtos. Por favor, verique '\
                    'verifique quais produtodos n??o temos estoque.'

            if error_msg_inventory:
                messages.error(
                    self.request,
                    error_msg_inventory
                )

                self.request.session.save()
                return redirect('product:cart')

        qtd_total_cart = utils.cart_total_qtd(cart)
        value_total_cart = utils.cart_totals(cart)

        order = Order(
            user=self.request.user,
            total_price=value_total_cart,
            qtd_total=qtd_total_cart,
            status='C'
        )

        order.save()

        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product=v['product_name'],
                    product_id=v['product_id'],
                    variation=v['variation_name'],
                    variation_id=v['variation_id'],
                    price=v['quantitative_price'],
                    promotional_price=v['promotional_quantitative_price'],
                    quantity=v['quantity'],
                    image=v['image']
                ) for v in cart.values()
            ]
        )

        del self.request.session['cart']

        return redirect(
            reverse(
                'order:pay',
                kwargs={'pk': order.id}
            )
        )


class Details(DispatchLoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'order/details.html'
    pk_url_kwarg = 'pk'


class ListOrders(DispatchLoginRequiredMixin, ListView):
    model = Order
    template_name = 'order/list.html'
    context_object_name = 'orders'
    paginate_by = 3
    ordering = ['-id']
