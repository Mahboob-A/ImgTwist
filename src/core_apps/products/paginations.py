from rest_framework.pagination import PageNumberPagination


class ProductsPageNumberPagination(PageNumberPagination):
    """Pagination class for core_apps.products.models.Products"""

    page_size = 10
    page_query_param = "page"
    max_page_size = 25
