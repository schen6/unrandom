from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25  # Default page size
    page_size_query_param = 'page_size'  # Allow client to override the page size
    max_page_size = 100  # Maximum limit for page size
