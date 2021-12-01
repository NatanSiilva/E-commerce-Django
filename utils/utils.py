def format_price(value):
    return f'R$ {value:.2f}'.replace('.', ',')


def cart_total_qtd(cart):
    return sum(cart_item['quantity'] for cart_item in cart.values())


def cart_totals(carrinho):
    return sum(
        [
            item.get('promotional_quantitative_price')
            if item.get('promotional_quantitative_price')
            else item.get('quantitative_price')
            for item
            in carrinho.values()
        ]
    )
