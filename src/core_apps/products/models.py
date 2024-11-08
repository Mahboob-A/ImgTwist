from django.db import models
from django.utils.translation import gettext_lazy as _

from core_apps.common.models import TimeStampModel


class Category(TimeStampModel):
    """Model for Product Category"""

    name = models.CharField(
        verbose_name=_("Category Name"), max_length=255, db_index=True
    )
    description = models.TextField(
        verbose_name=_("Category Description"), blank=True, null=True
    )


class BrandName(TimeStampModel):
    """Model for Product Brand Name"""

    categories = models.ManyToManyField(Category, related_name="brands")
    name = models.CharField(verbose_name=_("Brand Name"), max_length=255)
    description = models.TextField(
        verbose_name=_("Brand Description"), blank=True, null=True
    )


class Product(TimeStampModel):
    """Model for Product"""

    categories = models.ManyToManyField(Category, related_name="products")
    name = models.CharField(verbose_name=_("Product Name"), max_length=255)
    description = models.TextField(
        verbose_name=_("Product Description"), blank=True, null=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["name", "price"]),
        ]

    def __str__(self):
        return self.name

    @property
    def get_product_name(self):
        return self.name


class ProductImages(TimeStampModel):
    """Model for Product Images"""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products/images")
