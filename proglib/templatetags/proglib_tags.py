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


@register.inclusion_tag('proglib/inc/_item_status.html')
def item_status(*args, **kwargs):
    item_object = kwargs['item_object']
    if item_object.status == 'agreement':
        status_color = 'text-info'
    elif item_object.status == 'editing':
        status_color = 'text-warning'
    elif item_object.status == 'actual':
        status_color = 'text-primary'
    elif item_object.status == 'not_actual':
        status_color = 'text-secondary'
    elif item_object.status == 'not_used':
        status_color = 'text-danger'
    elif item_object.status == 'operating':
        status_color = 'text-primary'
    elif item_object.status == 'priority':
        status_color = 'text-success'
    else:
        status_color = 'text-white bg-dark'

    context = {
        'status_color': status_color,
        'object': item_object
    }
    return context
