from rest_framework import pagination
from rest_framework.response import Response


class RealEstate2022Paginator(pagination.PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response(pagination.OrderedDict([
            ('count', self.page.paginator.count),
            ('total_pages', int(self.page.paginator.count / self.page_size) + 1),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
        ]))

    # def get_paginated_response(self, data):
    #     return Response(OrderedDict([
    #         ('count', self.page.paginator.count),
    #         ('next', self.get_next_link()),
    #         ('previous', self.get_previous_link()),
    #         ('results', data)
    #     ]))