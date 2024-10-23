from django.utils.deprecation import MiddlewareMixin

class TokenPrefixMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header and not auth_header.startswith('Token '):
            request.META['HTTP_AUTHORIZATION'] = f'Token {auth_header}'