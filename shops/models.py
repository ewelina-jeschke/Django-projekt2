# Django
from datetime import datetime

from django.db import models

from users.models import ExtendedUser


class BaseObject(models.Model):
    hidden = models.BooleanField('Ukryty', default=False)
    deleted = models.BooleanField('Usunięty', default=False)

    class Meta:
        abstract = True


class Address(models.Model):
    local_no = models.CharField(
        'nr lokalu',
        max_length=10,
        blank=True,
    )
    building = models.CharField(
        'nr budynku',
        max_length=10,
    )
    street = models.CharField(
        'ulica',
        max_length=40,
    )
    city = models.CharField(
        'miasto',
        max_length=40,
    )
    zip_code = models.CharField(
        'kod pocztowy',
        max_length=10,
    )

    def __str__(self):
        local = f'/{self.local_no}' if self.local_no else ''
        return f'{self.street} {self.building}/{self.local_no}, {self.zip_code} {self.city}'

    class Meta:
        verbose_name = 'adres'
        verbose_name_plural = 'adresy'
        ordering = []


class Warehouse(models.Model):
    name = models.CharField(
        'nazwa',
        max_length=10,
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        verbose_name='adres',
    )
    capacity = models.IntegerField('ilość produktów')


class Shop(models.Model):
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    name = models.CharField('nazwa', max_length=50)


class Status(models.Model):
    name = models.CharField('nazwa', max_length=50)

    def __str__(self):
        return self.name


class Order(models.Model):

    number = models.CharField('numer zamówienia', max_length=50)
    shipping_address = models.ForeignKey(
        Address,
        verbose_name='adres do wysyłki',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='shipping_addresses'
    )
    invoice_address = models.ForeignKey(
        Address,
        verbose_name='adres do faktury',
        on_delete=models.PROTECT,
        related_name='invoice_addresses'
    )
    status = models.ForeignKey(
        Status,
        verbose_name='status',
        on_delete=models.CASCADE,
    )
    created_date = models.DateField(
        'data utworzenia',
        blank=True,
        null=True,
        auto_now_add=True,
    )
    client = models.ForeignKey(
        ExtendedUser,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )


class Discount(models.Model):
    pass


class ShippingMethod(models.Model):
    name = models.CharField('nazwa', max_length=50)
    price = models.DecimalField('kwota wysyłki', decimal_places=2, max_digits=5)


class PaymentMethod(models.Model):
    name = models.CharField('nazwa', max_length=50)


class Product(models.Model):
    name = models.CharField('nazwa', max_length=50, blank=True)
    order = models.ForeignKey(Order, verbose_name='zamówienie', on_delete=models.CASCADE)
    in_stock = models.IntegerField('stan magazynowy')
    price = models.DecimalField(
        'cena produktu',
        decimal_places=2,
        max_digits=5,
        blank=True,
        null=True,
    )


class Invoice(BaseObject):
    number = models.CharField('numer', max_length=50)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_date = models.DateField('data utworzenia', auto_now_add=True)
    payment_date = models.DateField('termin płatności')


