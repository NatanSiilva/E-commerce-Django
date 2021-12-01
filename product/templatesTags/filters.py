from django.template import Library
from utils import utils

register = Library()


@register.filter
def format_price(value):
    return utils.format_price(value)


@register.filter
def cart_total_qtd(cart):
    return utils.cart_total_qtd(cart)


@register.filter
def cart_totals(carrinho):
    return utils.cart_totals(carrinho)
