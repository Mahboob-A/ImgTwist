from django.urls import path

from core_apps.products.views import RetriveProductAPIView, RetriveProductListAPIView, ProductCreateUpdateDeleteAPIView, ProductImageDeleteAPIView, CategoryAPIView

urlpatterns = [
    
    # Products
    path("product/<uuid:product_id>/", RetriveProductAPIView.as_view(), name="get_single_product"),
    path("create/", ProductCreateUpdateDeleteAPIView.as_view(), name="create_product"),
    path("update/<uuid:product_id>/", ProductCreateUpdateDeleteAPIView.as_view(), name="update_product"),
    path("delete/<uuid:product_id>/", ProductCreateUpdateDeleteAPIView.as_view(), name="delete_product"),
    
    path("all/", RetriveProductListAPIView.as_view(), name="get_all_products"),
    
    path("delete/<uuid:product_id>/product-image-delete/", ProductImageDeleteAPIView.as_view(), name="delete_product_image"),
    
    # Categoty 
    path("category/<uuid:category_id>/", CategoryAPIView.as_view(), name="category"),
    path("category/all/", CategoryAPIView.as_view(), name="category"),
    path("category/create/", CategoryAPIView.as_view(), name="category"),
    path("category/update/<uuid:category_id>/", CategoryAPIView.as_view(), name="category_detail"),
    path("category/delete/<uuid:category_id>/", CategoryAPIView.as_view(), name="category_detail"),
]