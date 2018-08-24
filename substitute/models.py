from django.db.models import Model, BigIntegerField, CharField, ManyToManyField
from django.contrib.auth.models import User


class Product(Model):
    code = BigIntegerField("code produit", unique=True, null=True)
    name = CharField("nom", max_length=200)
    nutriscore = CharField("nutriscore", max_length=10, null=True)
    url_picture = CharField("image", max_length=200, null=True)
    users = ManyToManyField(User, related_name="products")

    class Meta:
        verbose_name = "produits enregistrés"

    def __str__(self):
        return self.name
