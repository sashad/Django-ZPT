# Django-ZPT
ZPT (TAL) to Django. Original templates are awful :)

views.py example, TAL_templates directory in project root:
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
