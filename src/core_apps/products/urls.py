from django.urls import path

from core_apps.products.views import RetriveProductAPIView, RetriveProductListAPIView, ProductCreateUpdateDeleteAPIView, ProductImageDeleteAPIView

urlpatterns = [
    path("product/<uuid:product_id>/", RetriveProductAPIView.as_view(), name="get_single_product"),
    path("create/", ProductCreateUpdateDeleteAPIView.as_view(), name="create_product"),
    path("update/<uuid:product_id>/", ProductCreateUpdateDeleteAPIView.as_view(), name="update_product"),
    path("delete/<uuid:product_id>/", ProductCreateUpdateDeleteAPIView.as_view(), name="delete_product"),
    
    path("all/", RetriveProductListAPIView.as_view(), name="get_all_products"),
    
    path("delete/<uuid:product_id>/product-image-delete/", ProductImageDeleteAPIView.as_view(), name="delete_product_image"),
    
    
]