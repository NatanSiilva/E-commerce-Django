# Generated by Django 3.2.9 on 2021-11-23 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/%y/%m', verbose_name='Imagem'),
        ),
        migrations.AlterField(
            model_name='product',
            name='long_description',
            field=models.TextField(verbose_name='Descrição longa'),
        ),
        migrations.AlterField(
            model_name='product',
            name='marketing_price',
            field=models.FloatField(verbose_name='Preço de venda'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='product',
            name='promotional_marketing_price',
            field=models.FloatField(default=0.0, verbose_name='Preço de venda promocional'),
        ),
        migrations.AlterField(
            model_name='product',
            name='short_description',
            field=models.TextField(max_length=255, verbose_name='Descrição curta'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('V', 'Variação'), ('S', 'Simples')], default='V', max_length=1, verbose_name='Tipo'),
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nome')),
                ('price', models.FloatField(verbose_name='Preço')),
                ('promotional_price', models.FloatField(default=0.0, verbose_name='Preço de venda')),
                ('inventory', models.PositiveIntegerField(default=1, verbose_name='Estoque')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]