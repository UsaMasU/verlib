from django import template
from proglib.models import *

register = template.Library()


@register.inclusion_tag('proglib/inc/_library_tree.html')
def library_tree():
    lib_tree = LibraryTree.objects.all()
    return {"lib_tree": lib_tree}


@register.inclusion_tag('proglib/inc/_snippet_card_small.html')
def card_small(*args, **kwargs):
    context = {
        'object': kwargs['object'],
    }
    return context