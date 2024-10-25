from django.db import models

# Create your models here.


class product(models.Model):
    product_title = models.CharField(max_length=100, unique=True)
    amount = models.PositiveIntegerField()
    exchaged = models.PositiveIntegerField()
    product_point = models.IntegerField()
    product_image = models.ImageField(upload_to="product_image")
    product_description = models.CharField(max_length=100)
    product_category = models.ManyToManyField(
        "product_category", related_name="product_category", blank=True
    )

    def __str__(self):
        return self.product_title


# for recommend
class product_category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name
