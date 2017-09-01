from __future__ import absolute_import

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.test import signals

from jinja2 import Environment
from jinja2 import Template as Jinja2Template

ORIGINAL_JINJA2_RENDERER = Jinja2Template.render


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env


# This code can be run only once
def instrumented_render(template_object, *args, **kwargs):
    context = dict(*args, **kwargs)
    signals.template_rendered.send(
        sender=template_object,
        template=template_object,
        context=context)
    return ORIGINAL_JINJA2_RENDERER(template_object, *args, **kwargs)


Jinja2Template.render = instrumented_render
