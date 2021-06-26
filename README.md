# Django-ZPT
ZPT (TAL) to Django. Original templates are awful :)

"Zope Page Templates provide an elegant templating mechanism that achieves a clean separation of presentation and application logic while allowing for designers to work with templates in their visual editing tools (FrontPage, Dreamweaver, GoLive, etc.)."

[Chameleon](https://chameleon.readthedocs.io/en/latest/) - "The language used is page templates, originally a Zope invention, but available here as a standalone library that you can use in any script or application running Python 2.7 and up, including 3.4+ and pypy). It comes with a set of new features, too."

```
pip install chameleon
```

Copy Chameleon folder in your Djanjo project.

Copy app_site_ru and TAL_templates folders same way for a test.

Edit settings.py:
```
TEMPLATES = [
    {
        'NAME': 'Chameleon',
        'BACKEND': 'Chameleon.backends.ChameleonTemplates',
        'DIRS': ['TAL_templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
    {
        'NAME': 'Django',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

Edit url.py:

```
urlpatterns = [
	path('zpt/', include('app_site_ru.urls')), # for a test
	path('admin/', admin.site.urls),
]
```

views.py example, TAL_templates is a directory in project root:
```
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import engines, RequestContext, Template

import logging

def from_file(request):
    chameleon_engine = engines['Chameleon']
    pt = chameleon_engine.get_template('TAL_templates/test.pt')
    return HttpResponse(pt.render({}, request))

def from_string(request):
    chameleon_engine = engines['Chameleon']
    pt = chameleon_engine.from_string('<html><body tal:content="context.hello"></body></html>')
    return HttpResponse(pt.render({"hello":"Hello, ZPT from string."}, request))

```

More complicated templates:

1. Define a template Common.pt with a macro (common)
```
<!DOCTYPE html>
<metal:block define-macro="common" >
<html>
        <body>
                <metal:block metal:define-slot="swiper_and_form" tal:omit-tag="">
                <!--============================== swiper and form ================================-->
                </metal:block>
                <metal:block metal:define-slot="services" tal:omit-tag="">
                <!--============================== For Our Clients / Services ================================-->
                </metal:block>
                <metal:block metal:define-slot="about_us" tal:omit-tag="">
                <!--============================== About Us ================================-->
                </metal:block>
                <metal:block metal:define-slot="products_and_gifts" tal:omit-tag="">
                <!--============================== Products & Gifts ================================-->
                </metal:block>
                <metal:block metal:define-slot="testimonials" tal:omit-tag="">
                <!--============================== Testimonials ================================-->
                </metal:block>
                <metal:block metal:define-slot="counters" tal:omit-tag="">
                <!--============================== Counters ================================-->
                </metal:block>
                <metal:block metal:define-slot="about_our_team" tal:omit-tag="">
                <!--============================== About Our Team ================================-->
                </metal:block>
                <metal:block metal:define-slot="owl_carousel" tal:omit-tag="">
                <!--============================== Owl Carousel ================================-->
                </metal:block>
                <metal:block metal:define-slot="news_and_tips" tal:omit-tag="">
                <!--============================== News & Tips ================================-->
                </metal:block>
                <metal:block metal:define-slot="contact_info" tal:omit-tag="">
                <!--============================== Contact info ================================-->
                </metal:block>
        </body>
</html>
</metal:block>
```

2. Define templates for every slot, example one (contact_info.pt):
```
        <!-- Contact info-->
        <a name="contacts"></a>
        <section class="section-60 text-center bg-gray-lighter">
          <div class="shell shell-fluid">
            <div class="range range-condensed range-bordered">
              <div class="cell-xs-6 cell-sm-3 height-fill offset-top-40 offset-sm-top-0">
                <div class="range-bordered-item">
                  <address class="contact-info contact-info-sm">
                    <div class="icon-wrap"><span class="icon icon-md icon-primary mdi mdi-email-outline"></span></div>
                    <div class="link-wrap"><a target="_blank" href="mailto:info@1vp.ru" class="link link-md link-gray-darker">info@1vp.ru</a></div>
                  </address>
                </div>
              </div>
              <div class="cell-xs-6 cell-sm-3 height-fill offset-top-40 offset-sm-top-0">
                <div class="range-bordered-item">
                  <address class="contact-info contact-info-sm">
                    <div class="icon-wrap"><span class="icon icon-md icon-primary mdi mdi-telegram"></span></div>
                    <div class="link-wrap"><a target="_blank" href="https://t.me/www_1vp_ru" class="link link-md link-gray-darker">@www_1vp_ru</a></div>
                  </address>
                </div>
              </div>
            </div>
          </div>
        </section>
```

3. So index.pt:
```
<metal:block tal:define="container load:Common.pt" metal:use-macro="python: container.macros.common">
    <tal:block metal:fill-slot="swiper_and_form" >
    </tal:block>
    <tal:block metal:fill-slot="services" >
    </tal:block>
    <tal:block metal:fill-slot="about_us" >
    </tal:block>
    <tal:block metal:fill-slot="products_and_gifts" >
    </tal:block>
    <tal:block metal:fill-slot="testimonials" >
    </tal:block>
    <tal:block metal:fill-slot="counters" >
    </tal:block>
    <tal:block metal:fill-slot="about_our_team" >
    </tal:block>
    <tal:block metal:fill-slot="owl_carousel" >
    </tal:block>
    <tal:block metal:fill-slot="news_and_tips" >
    </tal:block>
    <tal:block metal:fill-slot="contact_info" >
        <tal:block tal:define="info load:contact_info.pt" tal:replace="structure info()" />
    </tal:block>
</metal:block>
```

4. views.py example to build an index page:

```
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import engines
from random import random

def index(request):
    chameleon_engine = engines['Chameleon']
    pt = chameleon_engine.get_template('TAL_templates/index.pt')
    context = {'title': "Simple Smart Home"}
    context['description'] = """Простой Умный Дом. Построен на чипе esp8266 и шине 1-wire. Не требует программирования,
        готов к работе. Быстрая настройка через web браузер.
        Доступ через Интернет со смартфона, автоматическое обновление ПО.
    """
    context['lang'] = 'ru'
    context['canonical'] = 'https://home.1vp.ru/ru/'
    context['random'] = random

    return HttpResponse(pt.render(context, request))
```