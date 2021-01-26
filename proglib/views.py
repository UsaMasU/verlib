from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.list import MultipleObjectMixin
from proglib.models import LibraryTree, LibraryItem, PLC, Tag, HMI


def index(request):
    return render(request, 'proglib/index.html')


class PLCView(DetailView, MultipleObjectMixin):
    model = PLC
    template_name = 'proglib/plc_view.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        object_list = LibraryItem.objects.filter(plc__slug=self.object.slug)
        context = super(PLCView, self).get_context_data(object_list=object_list, **kwargs)
        context['page_title'] = kwargs['object'].title
        context['object_list'] = object_list
        print(object_list)
        return context


class HMIView(DetailView, MultipleObjectMixin):
    model = HMI
    template_name = 'proglib/hmi_view.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        object_list = LibraryItem.objects.filter(hmi__slug=self.object.slug)
        context = super(HMIView, self).get_context_data(object_list=object_list, **kwargs)
        context['page_title'] = kwargs['object'].title
        context['object_list'] = object_list
        return context


class TagView(DetailView, MultipleObjectMixin):
    model = Tag
    template_name = 'proglib/tag_view.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        object_list = LibraryItem.objects.filter(tag__slug=self.object.slug)
        context = super(TagView, self).get_context_data(object_list=object_list, **kwargs)
        context['page_title'] = kwargs['object'].title
        context['object_list'] = object_list
        print(object_list)
        return context

class CategoryView(DetailView, MultipleObjectMixin):
    model = LibraryTree
    template_name = 'proglib/category_view.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        object_list = LibraryItem.objects.filter(category__slug=self.object.slug)
        context = super(CategoryView, self).get_context_data(object_list=object_list, **kwargs)
        # print(kwargs['object'].title)
        # print(kwargs['object'].content)
        # print('list:', object_list)

        context['page_title'] = kwargs['object'].title
        context['object_list'] = object_list
        return context


class ItemView(DetailView):
    model = LibraryItem
    template_name = 'proglib/item_view.html'

    def get_context_data(self, **kwards):
        context = super(ItemView, self).get_context_data(**kwards)
        context['object_plc'] = context['object'].plc.prefetch_related().all()
        context['object_hmi'] = context['object'].hmi.prefetch_related().all()
        context['object_tag'] = context['object'].tag.prefetch_related().all()
        return context