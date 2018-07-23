from django.db import models

class Category(models.Model):
    name = models.CharField("nom", max_length=200, unique=True)

    class Meta:
        verbose_name = "catégorie"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField("nom", max_length=200, unique=True)
    nutriscore = models.CharField("nutriscore", max_length=10)
    generic_name = models.CharField("nom générique", max_length=200)
    url_picture = models.CharField("image", max_length=200)
    categories = models.ManyToManyField(Category,related_name="products", blank=True)

    class Meta:
        verbose_name = "produit"

    def __str__(self):
        return self.name
