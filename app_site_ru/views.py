from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import engines, RequestContext, Template

import logging
logger = logging.getLogger(__name__)

def from_file(request):
    chameleon_engine = engines['Chameleon']
    pt = chameleon_engine.get_template('TAL_templates/test.pt')
    return HttpResponse(pt.render({}, request))

def from_string(request):
    chameleon_engine = engines['Chameleon']
    pt = chameleon_engine.from_string('<html><body tal:content="context.hello"></body></html>')
    return HttpResponse(pt.render({"hello":"Hello, ZPT from string."}, request))
