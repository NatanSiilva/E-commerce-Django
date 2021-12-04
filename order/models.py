from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    total_price = models.FloatField(verbose_name='Preço Total')
    qtd_total = models.PositiveIntegerField()
    status = models.CharField(
        default='C',
        max_length=1,
        choices=(
            ('A', 'Aprovado'),
            ('C', 'Criado'),
            ('R', 'Reprovado'),
            ('P', 'Pendente'),
            ('E', 'Enviado'),
            ('F', 'Finalizado')
        )
    )

    def __str__(self):
        return f'Pedido Nº {self.pk}'

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Pedido')
    product = models.CharField(max_length=255, verbose_name='Produto')
    product_id = models.PositiveIntegerField(verbose_name='ID do Produto')
    variation = models.CharField(max_length=255, verbose_name='Variação')
    variation_id = models.PositiveIntegerField(verbose_name='ID da Variação')
    price = models.FloatField(verbose_name='Preço')
    promotional_price = models.FloatField(default=0, verbose_name='Preço Promocional')
    quantity = models.PositiveIntegerField(verbose_name='Quantidade')
    image = models.CharField(max_length=2000, verbose_name='Imagem')

    def __str__(self):
        return f'Item do {self.order}'

    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens do pedido'
