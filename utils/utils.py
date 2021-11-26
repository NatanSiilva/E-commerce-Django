def format_price(value):
    return f'R$ {value:.2f}'.replace('.', ',')


def cart_total_qtd(cart):
   return sum(cart_item['quantity'] for cart_item in cart.values())
