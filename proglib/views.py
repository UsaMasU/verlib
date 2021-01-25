from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.list import MultipleObjectMixin
from proglib.models import LibraryTree, LibraryItem


def index(request):
    return render(request, 'proglib/index.html')


class CategoryItem(DetailView, MultipleObjectMixin):
    model = LibraryTree
    template_name = 'proglib/category_detail.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        object_list = LibraryItem.objects.filter(category__slug=self.object.slug)
        context = super(CategoryItem, self).get_context_data(object_list=object_list, **kwargs)
        # print(kwargs['object'].title)
        # print(kwargs['object'].content)
        # print('list:', object_list)

        context['page_title'] = kwargs['object'].title
        context['object_list'] = object_list
        return context


class ItemDetail(DetailView):
    model = LibraryItem
    template_name = 'proglib/item_detail.html'

    def get_context_data(self, **kwards):
        context = super(ItemDetail, self).get_context_data(**kwards)
        context['object_plc'] = context['object'].plc.prefetch_related().all()
        context['object_hmi'] = context['object'].hmi.prefetch_related().all()
        context['object_tag'] = context['object'].tag.prefetch_related().all()
        return context