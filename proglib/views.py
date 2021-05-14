from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import DetailView, ListView
from django.views.generic.list import MultipleObjectMixin
from proglib.models import LibraryTree, LibraryItem, PLC, Tag, HMI, ItemAuthor
from .apps import ProglibConfig


class MainPage(ListView):
    template_name = 'proglib/index.html'

    def get(self, *args, **kwargs):
        #get_super = super().get(*args, **kwargs)

        paginator_upd = Paginator(LibraryItem.objects.filter(updated_at__lte=timezone.now()).order_by('-updated_at')[:10], 4)
        page_num_upd = self.request.GET.get('page_upd', 1)
        page_objects_upd = paginator_upd.get_page(page_num_upd)

        paginator_new = Paginator(LibraryItem.objects.filter(created_at__lte=timezone.now()).order_by('-created_at')[:10], 4)
        page_num_new = self.request.GET.get('page_new', 1)
        page_objects_new = paginator_new.get_page(page_num_new)

        context = {'upd_objects': page_objects_upd, 'new_objects': page_objects_new}
        return render(self.request, self.template_name, context)


class Search(ListView):
    template_name = 'proglib/search.html'
    paginate_by = 50
    context = {}

    def find(self, search_text, search_option):
        print('Processing FIND')
        search_obj_found = []
        if len(search_text) >= 3:
            if search_option == 'объект':
                search_text_reg = [
                    search_text.lower(),
                    search_text.capitalize(),
                    search_text.upper()
                ]
                for text in search_text_reg:
                    search_cat = LibraryTree.objects.filter(title__contains=text)
                    search_obj = LibraryItem.objects.filter(Q(title__contains=text) | Q(content__contains=text))
                    if len(search_cat) > 0:
                        for obj in search_cat:
                            search_obj_found.append(obj)
                    if len(search_obj) > 0:
                        for obj in search_obj:
                            search_obj_found.append(obj)
                # return search_obj
            elif search_option == 'категория':
                print('категория')
            elif search_option == 'текст':
                print('текст')
            else:
                print('no option')
        else:
            print('Недостаточно информации для поиска')
        print(search_obj_found)
        print('Finished processing FIND')
        return list(set(search_obj_found))


    def post(self, *args, **kwargs):
        print('Processing POST request')
        search_text = self.request.POST.get('search_text')
        search_option = self.request.POST.get('search_option')
        print('post_search_str:', search_text)
        print('post_search_parameter:', search_option)
        self.context['search_text'] = search_text
        self.context['object_list'] = self.find(search_text, search_option)
        print('Finished processing POST request')
        return render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        print('Processing GET request')
        # response = super().get(*args, **kwargs)
        search_text = self.request.GET.get('search_text')
        search_option = self.request.GET.get('search_option')
        print('get_search_str:', search_text)
        print('get_search_parameter:', search_option)

        # paginator_search = Paginator(LibraryItem.objects.filter(updated_at__lte=timezone.now()).order_by('-updated_at')[:10], 3)
        paginator_search = Paginator(self.find(search_text, search_option), self.paginate_by)
        page_num_search = self.request.GET.get('page', 1)
        page_objects_search = paginator_search.get_page(page_num_search)
        print('page_objects_search:', page_objects_search)
        for item in page_objects_search:
            print(item)
        #print('response:', response)
        print('Finished processing GET request')
        #return response

        context = {
            'objects': page_objects_search,
            'get_search_str': search_text,
            'get_search_parameter': search_option
        }
        print('context: ', context);
        return render(self.request, self.template_name, context)



    def get_queryset(self):
        print('Processing QUERYSET')

        search_text = self.request.GET.get('search_text')
        search_option = self.request.GET.get('search_option')

        print('queryset_search_str:', search_text)
        print('queryset_search_parameter:', search_option)

        print('Finished processing QUERYSET')
        return self.find(search_text, search_option)    # object_list

    def get_context_data(self, **kwargs):
        print('Processing CONТEXT_DATA')
        something = self.object_list
        print('object:', something)
        print("====================")
        for item in something:
            print(item.id, item.title)
        print("====================")
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
    model = ItemAuthor
    template_name = 'proglib/author_view.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        object_list = LibraryItem.objects.filter(author__slug=self.object.slug)
        context = super(ItemAuthorView, self).get_context_data(object_list=object_list, **kwargs)
        context['page_title'] = kwargs['object'].name
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


def search(request):
    template = 'proglib/search.html'
    name_url = request.resolver_match.url_name
    context = {}

    if request.method == 'POST':
        if 'search_text' in request.POST:
            if request.POST['search_option'] == 'объект':
                search_text = [
                    request.POST['search_text'].lower(),
                    request.POST['search_text'].capitalize(),
                    request.POST['search_text'].upper()
                ]
                search_obj_found = []

                context['search_text'] = request.POST['search_text']

                for text in search_text:
                    search_obj = LibraryItem.objects.filter(Q(title__contains=text) | Q(content__contains=text))
                    if len(search_obj) > 0:
                        for obj in search_obj:
                            search_obj_found.append(obj)
                    if len(search_obj_found):
                        context['object_list'] = set(search_obj_found)
                return render(request, template, context)
            elif request.POST['search_option'] == 'метка':
                print('метка')
            elif request.POST['search_option'] == 'текст':
                print('текст')
            else:
                print('no option')
    else:
        print('get from func...')
        return render(request, template, context)