from rest_framework import pagination


class RealEstate2022Paginator(pagination.PageNumberPagination):
    page_size = 10