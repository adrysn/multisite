from importlib import import_module

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.http.request import split_domain_port


class MultiSiteMiddleware:

    OVERRIDING_FIELDS = frozenset({
        'TEST_TITLE',
    })

    OVERLOADING_MATCHING_TABLE = {
        'site1.local': 'site1.mysite.com',
        'site2.local': 'site2.mysite.com',
    }

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        domain, _ = split_domain_port(request.get_host())

        # Get the production domain corresponding to the current site in dev mode.
        if settings.DEBUG:
            try:
                domain = MultiSiteMiddleware.OVERLOADING_MATCHING_TABLE[domain]
            except KeyError:
                raise ImproperlyConfigured(
                    f'No matching overloaded domain for {domain}'
                )

        # Get current site object and set SITE_ID.
        try:
            current_site = Site.objects.get(domain=domain)
        except Site.DoesNotExist:
            current_site = Site.objects.get(id=settings.DEFAULT_SITE_ID)
        request.current_site = current_site
        settings.SITE_ID = current_site.id
        settings.site_domain = domain

        # Determine the module path which contains site-wise assets.
        site_path = settings.site_domain.replace('.', '-')

        # Override settings.
        try:
            new_settings = import_module(f'overload.{site_path}.settings')
        except (ModuleNotFoundError, ImportError):
            new_settings = import_module(f'overload.default_settings')
        finally:
            for field in self.OVERRIDING_FIELDS:
                if hasattr(new_settings, field):
                    new_value = getattr(new_settings, field)
                    setattr(settings, field, new_value)

        # Override URL patterns.
        try:
            override_urls = import_module(f'overload.{site_path}.urls')
            if hasattr(override_urls, 'urlpatterns'):
                settings.override_urlpatterns = override_urls.urlpatterns
            request.urlconf = f'overload.{site_path}.urls'
        except ImportError:  # fallback to the default URL
            pass

        response = self.get_response(request)
        return response
