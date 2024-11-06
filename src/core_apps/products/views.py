from django.shortcuts import render
from django.shortcuts import get_object_or_404


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from core_apps.products.models import Category, BrandName, Product, ProductImages
from core_apps.products.serializers import CategorySerializer, BrandNameSerializer, ProductSerializer
from core_apps.products.renderers import ProductJSONRenderer, ProductsJSONRenderer


class ProductCreateUpdateDeleteAPIView(APIView):
    """API View for Product"""

    parser_classes = [MultiPartParser, FormParser]
    renderer_classes = [ProductJSONRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Create a new product"""

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, product_id):
        """Update a product"""

        if not product_id:
            return Response({"status": "error", "detail": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"status": "error", "detail": f"Product not found with the ID {product_id}"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(
            product, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id=None):
        """Delete a product"""

        if product_id is None:
            return Response({"status": "error", "detail": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"status": "error", "detail": f"Product not found with the ID {product_id}"}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response({"status": "success", "detail": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class RetriveProductAPIView(APIView):
    """API View to Retrive a Single Product Detail 
    
    NOTE: In order to seprate the renderer class strucutre, 
        the Retrive of Singel product and All products APIs are seprated.
    """
    renderer_classes = [ProductJSONRenderer]

    def get(self, request, product_id=None):
        """Retrive a product provided the product_id else retrive all products"""

        if product_id:
            try:
                product = Product.objects.get(id=product_id)
                serializer = ProductSerializer(product)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                return Response({"status": "error", "detail": f"Product not found with the ID {product_id}"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"status": "error", "detail": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)



class RetriveProductListAPIView(APIView):
    """API View for All Products"""

    renderer_classes = [ProductsJSONRenderer]

    def get(self, request):
        """Retrive All Products"""

        serializer = ProductSerializer(Product.objects.all(), many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class ProductImageDeleteAPIView(APIView):
    """API View for Product Image Delete
        Delete Product Image: Bulk Delete         
        Return: 
             - status: state of the operation - success/error 
    """
    renderer_classes = [ProductJSONRenderer]
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id=None):
        """Delete Product Images

            @params:
                    - product_id: Product ID
            Body:
                    - image_id: Image ID If a single Image to be Deleted
                    - image_ids: Image IDs if Multiple Images to be Deleted

        """

        if product_id is None:
            return Response({"status": "error", "detail": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"status": "error", "detail": f"Product not found with the ID {product_id}"}, status=status.HTTP_404_NOT_FOUND)

        image_id = request.data.get("image_id", None)
        image_ids = request.data.get("image_ids", [])
        if not image_id and not image_ids:
            return Response({"status": "error", "detail": "Image IDs for Bulk Delete or An Image ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        if image_id:
            try:
                image = ProductImages.objects.get(id=image_id)
                image.delete()
                return Response({"status": "success", "detail": "Image deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            except ProductImages.DoesNotExist:
                return Response({"status": "error", "detail": f"Image not found with the ID {image_id}"}, status=status.HTTP_404_NOT_FOUND)

        if image_ids:
            # ForeignKey: Product with ProductImages
            existing_images_ids = set(
                product.images.values_list("id", flat=True))
            invalid_ids = [iamge_id for iamge_id in existing_images_ids if iamge_id not in existing_images_ids]

            if invalid_ids:
                return Response(
                    {"status": "error", "detail": f"Image not related to {product.get_product_name} can not be deleted. Invalid image IDs are {invalid_ids}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            iamges = ProductImages.objects.filter(id__in=image_ids, product=product)
            images_delate_count, metadata = iamges.delete()

            if images_delate_count == 0:
                return Response({"status": "error", "detail": f"No images found with the IDs {image_ids} to Delete"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"status": "success", "detail": f"{images_delate_count} images deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
