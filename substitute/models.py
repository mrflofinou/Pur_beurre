from django.db.models import Model, BigIntegerField, CharField, ManyToManyField, ForeignKey, CASCADE
from django.contrib.auth.models import User


class Product(Model):
    code = BigIntegerField("code produit", unique=True, null=True)
    name = CharField("nom", max_length=200)
    nutriscore = CharField("nutriscore", max_length=10, null=True)
    url_picture = CharField("image", max_length=200, null=True)
    users = ManyToManyField(User, related_name="products")

    class Meta:
        verbose_name = "produit"

    def __str__(self):
        return self.name

class Query(Model):
    name = CharField("requete", max_length=200)
    user = ForeignKey(User, on_delete=CASCADE)
    product = ForeignKey(Product, on_delete=CASCADE, null=True)

    class Meta:
        verbose_name = "requetes"

    def __str__(self):
        return self.name