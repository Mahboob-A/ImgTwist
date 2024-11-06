import logging 

from django.shortcuts import render
from django.shortcuts import get_object_or_404


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from core_apps.products.models import Category, BrandName, Product, ProductImages
from core_apps.products.serializers import CategorySerializer, BrandNameSerializer, ProductSerializer
from core_apps.products.renderers import ProductJSONRenderer, ProductsJSONRenderer
from core_apps.products.paginations import ProductsPageNumberPagination


logger = logging.getLogger(__name__)

class ProductCreateUpdateDeleteAPIView(APIView):
    """API View for Product"""

    parser_classes = [MultiPartParser, FormParser]
    renderer_classes = [ProductJSONRenderer]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        """Create a new product"""

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            
            logger.info(f"\nProduct created: {serializer.data}")
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        
        logger.error(f"\nProduct creation failed: {serializer.errors}")
        return Response({"status": "error", "detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, product_id):
        """Update a product"""

        if not product_id:
            return Response({"status": "error", "detail": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            logger.error(f"\nProduct not found with the ID While Update {product_id}")
            return Response({"status": "error", "detail": f"Product not found with the ID {product_id}"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            
            logger.info(f"\nProduct updated: {serializer.data}")
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        logger.error(f"\nProduct update failed: {serializer.errors}")
        return Response({"status": "error", "detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id=None):
        """Delete a product"""

        if product_id is None:
            return Response({"status": "error", "detail": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            logger.error(f"\nProduct not found with the ID While Delete {product_id}")
            return Response({"status": "error", "detail": f"Product not found with the ID {product_id}"}, status=status.HTTP_404_NOT_FOUND)
        
        product.delete()
        logger.info(f"\nProduct deleted: {product_id}")
        return Response({"status": "success", "detail": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class RetriveProductAPIView(APIView):
    """API View to Retrive a Single Product Detail 
    
    NOTE: In order to seprate the renderer class strucutre, 
        the Retrive of Singel product and All products APIs are seprated.
    """
    renderer_classes = [ProductJSONRenderer]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
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


class RetriveProductListAPIView(ListAPIView):
    """API View for All Products"""

    renderer_classes = [ProductsJSONRenderer]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = ProductsPageNumberPagination

    def get(self, request, *args, **kwargs):
        """Retrive All Products"""
    
        paginated_queryset = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(paginated_queryset, many=True)
        
        return self.get_paginated_response({"status": "success", "data": serializer.data})


class ProductImageDeleteAPIView(APIView):
    """API View for Product Image Delete
        Delete Product Image: Bulk Delete         
        Return: 
             - status: state of the operation - success/error 
    """
    renderer_classes = [ProductJSONRenderer]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

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
                logger.info(f"\nProduct Single Image deleted: {image_id}")
                return Response({"status": "success", "detail": "Image deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            except ProductImages.DoesNotExist:
                return Response({"status": "error", "detail": f"Image not found with the ID {image_id}"}, status=status.HTTP_404_NOT_FOUND)

        if image_ids:
            # ForeignKey: Product with ProductImages
            existing_images_ids = set(
                product.images.values_list("id", flat=True))
            existing_images_ids = [str(id) for id in existing_images_ids]
            invalid_ids = [iamge_id for iamge_id in image_ids if iamge_id not in existing_images_ids]

            # print("existing: ", existing_images_ids)
            # print("invalid ids: ", invalid_ids)
            
            if invalid_ids:
                return Response(
                    {"status": "error", "detail": f"Image not related to {product.get_product_name} can not be deleted. Invalid image IDs are {invalid_ids}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            iamges = ProductImages.objects.filter(id__in=image_ids, product=product)
            images_delate_count, metadata = iamges.delete()

            if images_delate_count == 0:
                return Response({"status": "error", "detail": f"No images found with the IDs {image_ids} to Delete"}, status=status.HTTP_404_NOT_FOUND)
        
        logger.info(f"\nProduct Bulk Image deleted: {image_ids}")
        return Response({"status": "success", "detail": f"{images_delate_count} images deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class CategoryAPIView(APIView):
    """Minimal CRUD operations for Category.
    
    NOTE: Just Minimal APIs for time constraints. 
    """

    def get(self, request, category_id=None):
        """Retrieve a category or list of categories."""
        
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                serializer = CategorySerializer(category)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            except Category.DoesNotExist:
                logger.error(f"\nCategory with category_id {category_id} does not exist.")
                return Response({"status": "error", "detail": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new category."""
        
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            logger.info(f"\nCategory '{serializer.validated_data['name']}' created successfully.")
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        
        logger.error(f"\nError creating category: {e}")
        return Response({"status": "error", "detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
 
    def patch(self, request, category_id=None):
        """
        Update an existing category.
        """
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            logger.error(
                f"\nCategory with category_id {category_id} not found for update.")
            return Response({"status": "error", "detail": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            logger.info(f"\nCategory with category_id {category_id} updated successfully.")
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        logger.error(f"\nError updating category: {category_id}: {e}")
        return Response({"status": "error", "detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, category_id=None):
        """Delete a category."""
        
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
            
            logger.info(f"\nCategory with category_id {category_id} deleted successfully.")
            return Response({"status": "success", "detail": "Category deleted."}, status=status.HTTP_204_NO_CONTENT)
        
        except Category.DoesNotExist:
            logger.error(f"Category with category_id {category_id} does not exist.")
            return Response({"status": "error", "detail": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            logger.error(f"Error deleting category: {e}")
            return Response({"status": "error", "detail": "Something unexpected occured eleting category."}, status=status.HTTP_400_BAD_REQUEST)
