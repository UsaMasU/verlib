import string
import random

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from .models import LibraryTree, LibraryItem, PLC, HMI, Tag
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin


def clone_db_obj(modeladmin, request, queryset):
    for obj_field in queryset:
        str_rnd = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        obj_field.pk = None
        obj_field.title = ''.join([obj_field.title, '_', str_rnd])
        obj_field.slug = slugify(obj_field.title)
        obj_field.save()


clone_db_obj.short_description = "Дублировать обьект"


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True


admin.site.register(Tag, TagAdmin)


class PLCAdminForm(forms.ModelForm):
    content = forms.CharField(label='Описание', required=False, widget=CKEditorUploadingWidget())

    class Meta:
        model = PLC
        fields = '__all__'


class PLCAdmin(admin.ModelAdmin):
    form = PLCAdminForm
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True
    actions = [clone_db_obj]


admin.site.register(PLC, PLCAdmin)


class HMIAdminForm(forms.ModelForm):
    content = forms.CharField(label='Описание', required=False, widget=CKEditorUploadingWidget())

    class Meta:
        model = HMI
        fields = '__all__'


class HMIAdmin(admin.ModelAdmin):
    form = HMIAdminForm
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True
    actions = [clone_db_obj]

admin.site.register(HMI, HMIAdmin)


class LibraryTreeAdminForm(forms.ModelForm):
    content = forms.CharField(label='Описание', required=False, widget=CKEditorUploadingWidget())

    class Meta:
        model = LibraryTree
        fields = '__all__'


class LibraryTreeAdmin(admin.ModelAdmin):
    form = LibraryTreeAdminForm
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


# admin.site.register(LibraryTree, MPTTModelAdmin)
admin.site.register(
    LibraryTree,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
    ),
    list_display_links=(
        'indented_title',
    ),
    form = LibraryTreeAdminForm,
    prepopulated_fields={'slug': ('title', )},
)


class LibraryItemAdminForm(forms.ModelForm):
    content = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    links = forms.CharField(label='Ссылки', required=False, widget=CKEditorUploadingWidget())
    implements = forms.CharField(label='Применение', required=False, widget=CKEditorUploadingWidget())


    class Meta:
        model = LibraryItem
        fields = '__all__'


class LibraryItemAdmin(admin.ModelAdmin):
    form = LibraryItemAdminForm
    list_display = ('id', 'title', 'func', 'category', 'created_at', 'updated_at', 'is_published', 'get_photo', 'version')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content','func')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')
    #fields = ('title', 'category', 'content','plc', 'messages', 'links', 'implements', 'photo', 'get_photo', 'is_published', 'created_at', 'updated_at')
    readonly_fields = ('get_photo', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('category', 'title', 'func', 'version')}
    save_on_top = True
    actions = [clone_db_obj]

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        else:
            return '-'

    get_photo.short_description = 'Миниатюра'


admin.site.register(LibraryItem, LibraryItemAdmin)


admin.site.site_title = 'Управление библиотекой'
admin.site.site_header = 'Управление библиотекой'
