from importlib import import_module
from pkgutil import walk_packages

from django.apps import apps
from django.conf import settings
from django.template import TemplateDoesNotExist
from django.template.context import make_context
from django.template.engine import Engine
from django.template.library import InvalidTemplateLibrary

from chameleon import PageTemplateLoader, PageTemplateFile, PageTextTemplate
import os

import logging
logger = logging.getLogger(__name__)

from django.template.backends.base import BaseEngine
class ChameleonTemplates(BaseEngine):

    app_dirname = 'TAL_templates'

    def __init__(self, params):
        params = params.copy()
        options = params.pop('OPTIONS').copy()
        options.setdefault('autoescape', True)
        options.setdefault('debug', settings.DEBUG)
        options.setdefault('file_charset', 'utf-8')
        libraries = options.get('libraries', {})
        super().__init__(params)
        #self.__init__(params)
        self.engine = Engine(self.dirs, self.app_dirs, **options)
        self.templates = {}
        if ( not settings.DEBUG ):
            # if not DEBUG read all tal templates
            for DIR in params.get('DIRS', [self.app_dirname]):
                if ( params.get('APP_DIRS') ):
                    self.templates[DIR] = PageTemplateLoader(os.path.join(settings.BASE_DIR, DIR))
        #logger.debug(f"{__name__}: {self.templates=}")

    def from_string(self, template_code):
        return Template(PageTextTemplate(template_code), self)

    def get_template(self, template_name):
        #logger.debug(f"{__name__}: Get Template '{template_name}'")
        try:
            DIR, tname = template_name.split('/')[-2:]
        except:
            DIR = self.app_dirname
            tname = template_name

        if ( settings.DEBUG ):
            # reload a chameleon tenplate from FS, not need to restart the server
            t = PageTemplateFile(os.path.join(settings.BASE_DIR, DIR, tname), default_expression='python')
            pass
        else:
            t = self.templates[DIR][tname]
        try:
            return Template(t, self)
        except TemplateDoesNotExist as exc:
            reraise(exc, self)


class Template:

    def __init__(self, template, backend):
        #logger.debug(f"{__name__}: {template=} {backend=}")
        self.template = template
        self.backend = backend

    @property
    def origin(self):
        return self.template.origin

    def render(self, context=None, request=None):
        #logger.debug(f"{__name__}: {context=} {request=}")
        # add popular sections in context
        context["USER"] = request.user
        context["META"] = dict(request.META.items())
        context["GET"] = dict(request.GET.items())
        context["POST"] = dict(request.POST.items())
        context["FILES"] = dict(request.FILES.items())
        context["COOKIES"] = dict(request.COOKIES.items())
        try:
            return self.template(context=context, request=request)
        except TemplateDoesNotExist as exc:
            reraise(exc, self.backend)

