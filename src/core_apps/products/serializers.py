from rest_framework import serializers

from core_apps.products.models import BrandName, Category, Product, ProductImages


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category"""

    class Meta:
        model = Category
        fields = ["id", "name", "description"]


class BrandNameSerializer(serializers.ModelSerializer):
    """Serializer for BrandName"""

    class Meta:
        model = BrandName
        fields = ["id", "name", "description"]


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for ProductImages"""

    class Meta:
        model = ProductImages
        fields = ["id", "image", "created_at"]


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product"""

    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(use_url=True), write_only=True, required=False
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "quantity",
            "images",
            "uploaded_images",
        ]

    def validate_uploaded_images(self, value):
        max_size = 10 * 1024 * 1024  # 10 MB
        allowed_type = ["image/jpeg", "image/png", "image/gif", "image/webp"]
        errors = []
        for image in value:
            if image.size > max_size:
                max_size_in_mb = max_size / (1024 * 1024)
                image_size_in_mb = image.size / (1024 * 1024)
                errors.append(
                    f"Image {image.name} is too large. Max size is {max_size_in_mb: .2f} MB. The Image size is {image_size_in_mb: .2f} MB."
                )
            if image.content_type not in allowed_type:
                errors.append(
                    f"Image {image.name} is not a valid image type. Allowed types are {', '.join(allowed_type)}."
                )
        if errors:
            # print("error: ", errors)
            raise serializers.ValidationError(errors)

        return value

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", [])
        product = Product.objects.create(**validated_data)

        for image in uploaded_images:
            ProductImages.objects.create(product=product, image=image)

        return product

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", [])

        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.price = validated_data.get("price", instance.price)
        instance.quantity = validated_data.get("quantity", instance.quantity)
        instance.save()

        if uploaded_images:
            for image in uploaded_images:
                ProductImages.objects.create(product=instance, image=image)

        return instance


class CategorySerializer(serializers.ModelSerializer):
    """Serializers for Category"""

    class Meta:
        model = Category
        fields = ["id", "name", "description"]
