from pathlib import Path

from django.conf import settings
from django.core.exceptions import SuspiciousFileOperation
from django.template import Origin, TemplateDoesNotExist
from django.template.loaders.base import Loader
from django.utils._os import safe_join


class MultiSiteLoader(Loader):
    """
    Load domain-specific templates from `overload` directory.
    """
    def get_template_sources(self, template_name):
        """
        A method that takes a template_name and yields Origin instances for
        each possible source.
        """
        domain = settings.site_domain
        template_dir = (Path(settings.BASE_DIR) / 'overload' /
                        domain.replace('.', '-') / 'templates').resolve()
        template_dir = str(template_dir)
        name = safe_join(template_dir, template_name)
        yield Origin(
            name=name,
            template_name=template_name,
            loader=self,
        )

    def get_contents(self, origin):
        """
        Returns the contents for a template given a Origin instance.
        """
        try:
            with open(origin.name, encoding=self.engine.file_charset) as fp:
                return fp.read()
        except FileNotFoundError:
            raise TemplateDoesNotExist(origin)
