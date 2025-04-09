class NgrokAllowedHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request) :
        host = request.META.get('HTTP_HOST', '')
        from django.conf import settings

        if '.ngrok-free.app' in host and host not in settings.ALLOWED_HOSTS:
            settings.ALLOWED_HOSTS.append(host)

            if hasattr(settings, 'CSRF_TRUSTED_ORIGINS'):
                settings.CSRF_TRUSTED_ORIGINS.append(f'https://{host}')
            print(f'Added {host} to ALLOWED_HOSTS')
        return self.get_response(request)