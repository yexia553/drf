from rest_framework.pagination import PageNumberPagination as PNPG


class PageNumberPagination(PNPG):
    '''
    自定义分页类
    '''
    page_query_param = 'page'  # 前端查询某一页的参数名，如/books/bookinfos/?page=2
    page_size_query_param = 'page_size'  # 前端指定每一页返回的数据的条数，如/books/bookinfos/?page_size=100
    page_size = 5  # 后端默认设置的每页返回的数据的条数
    max_page_size = 5  # 前端允许的最大自定义每页的数据条数，也就是上面page_size的最大值
