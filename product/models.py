from django.db import models
from django.conf import settings
from django.utils.text import slugify
from utils import utils
from PIL import Image
import os


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nome')
    short_description = models.TextField(
        max_length=255, verbose_name='Descrição curta')
    long_description = models.TextField(verbose_name='Descrição longa')
    image = models.ImageField(
        upload_to='product_images/%y/%m', blank=True, null=True, verbose_name='Imagem')
    slug = models.SlugField(verbose_name='Slug',
                            unique=True, null=True, blank=True)
    marketing_price = models.FloatField(verbose_name='Preço de venda')
    promotional_marketing_price = models.FloatField(
        default=0.00, verbose_name='Preço de venda promocional')
    type = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variável'),
            ('S', 'Simples'),
        ),
        verbose_name='Tipo'
    )

    def get_price_format(self):
        return utils.format_price(self.marketing_price)
    get_price_format.short_description = 'Preço de venda'

    def get_promotional_price_format(self):
        return utils.format_price(self.promotional_marketing_price)
    get_promotional_price_format.short_description = 'Preço promocional'

    @staticmethod
    def resize_image(img, new_width=800):
        image_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        image_pil = Image.open(image_full_path)
        original_width, original_height = image_pil.size

        if original_width <= new_width:
            image_pil.close()
            return

        new_height = round((new_width * original_height) / original_width)

        new_image = image_pil.resize((new_width, new_height), Image.LANCZOS)
        new_image.save(
            image_full_path,
            optimize=True,
            quality=50
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.name)}'
            self.slug = slug

        super().save(*args, **kwargs)

        max_image_size = 800

        if self.image:
            self.resize_image(self.image, max_image_size)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=50, verbose_name='Nome', blank=True, null=True)
    price = models.FloatField(verbose_name='Preço',)
    promotional_price = models.FloatField(
        default=0.00, verbose_name='Preço de promocional')
    inventory = models.PositiveIntegerField(verbose_name='Estoque', default=1)

    def __str__(self):
        return self.name or self.product.name

    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'
