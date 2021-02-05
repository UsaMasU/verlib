from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.list import MultipleObjectMixin
from proglib.models import LibraryTree, LibraryItem, PLC, Tag, HMI
from .apps import ProglibConfig

def index(request):
    return render(request, 'proglib/index.html')


class Search(ListView):
    template_name = 'search.html'
    paginate_by = 3

    def get(self, *args, **kwargs):
        print('Processing GET request')
        response = super().get(*args, **kwargs)
        s_input = self.request.GET.get('s_input')
        s_select = self.request.GET.get('s_select')
        print('search_str:', s_input)
        print('search_parameter:', s_select)
        #print('response:', response)
        print('Finished processing GET request')
        return response

    def get_queryset(self):
        print('Processing QUERYSET')

        s_input = self.request.GET.get('s_input')
        s_select = self.request.GET.get('s_select')
        # qs.filter(name__startswith=self.kwargs.name)
        if len(s_input) == 0:
            print('Пустое поле')

        if s_select == 'объект':
            pass
        elif s_select == 'метка':
            pass
        elif s_select == 'текст':
            pass
        else:
            pass

        print('search_str:', s_input)
        print('search_parameter:', s_select)

        #object_list = LibraryItem.objects.all()

        print('Finished processing QUERYSET')
        return [s_input, s_select]  # object_list

    def get_context_data(self, **kwargs):
        something = self.object_list
        print('object:', something)
        print('Processing CONТEXT_DATA')
        data = super().get_context_data(**kwargs)
        data['page_title'] = 'Authors'
        print('Finished processing CONТEXT_DATA')
        return data


class PLCView(DetailView, MultipleObjectMixin):
    model = PLC
    template_name = 'proglib/plc_view.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        object_list = LibraryItem.objects.filter(plc__slug=self.object.slug)
        context = super(PLCView, self).get_context_data(object_list=object_list, **kwargs)
        context['page_title'] = kwargs['object'].title
        context['object_list'] = object_list
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


class ItemAuthorView(DetailView, MultipleObjectMixin):
    model = Tag
    template_name = 'proglib/tag_view.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        object_list = LibraryItem.objects.filter(tag__slug=self.object.slug)
        context = super(ItemAuthorView, self).get_context_data(object_list=object_list, **kwargs)
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

    def get_context_data(self, **kwargs):
        context = super(ItemView, self).get_context_data(**kwargs)
        context['object_plc'] = context['object'].plc.prefetch_related().all()
        context['object_hmi'] = context['object'].hmi.prefetch_related().all()
        context['object_tag'] = context['object'].tag.prefetch_related().all()
        context['object_author'] = context['object'].author.prefetch_related().all()
        context['object_edit_link'] = ''.join(['admin/', ProglibConfig.name, '/', (self.model.__name__).lower(),'/', str(kwargs['object'].id), '/change/'])
        return context