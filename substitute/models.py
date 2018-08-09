from django.db import models


class Product(models.Model):
    code = models.IntegerField("code produit", unique=True, null=True)
    name = models.CharField("nom", max_length=200)
    nutriscore = models.CharField("nutriscore", max_length=10)
    url_picture = models.CharField("image", max_length=200, null=True)
    ingredients = models.CharField("liste d'ingredients", max_length=1000, null=True)
    url_nutrition = models.CharField("valeurs nutritionnelles", max_length=200, null=True)
    stores = models.CharField("magasins", max_length=200, null=True)

    class Meta:
        verbose_name = "produits enregistrés"

    def __str__(self):
        return self.name
