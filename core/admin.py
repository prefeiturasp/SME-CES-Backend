from django.contrib import admin

from .models import Coordenadoria, Sistema, Modulo, SubModulo, Recurso

admin.site.register(Coordenadoria)


class SubModuloInline(admin.TabularInline):
    model = SubModulo
    extra = 0


@admin.register(Recurso)
class RecursoAdmin(admin.ModelAdmin):

    list_display = ('nome', 'sistema', 'rota', )
    search_fields = ('uuid', 'nome', 'sistema__nome')
    readonly_fields = ('uuid', 'id')
    raw_id_fields = ('sistema', 'modulo', 'submodulo',)


@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):

    list_display = ('nome', 'sistema', )
    search_fields = ('uuid', 'nome', 'sistema__nome')
    readonly_fields = ('uuid', 'id')
    inlines = [SubModuloInline, ]


@admin.register(Sistema)
class SistemaAdmin(admin.ModelAdmin):

    list_display = ('nome', 'coordenadoria', )
    search_fields = ('uuid', 'nome',)
    list_filter = (
        'coordenadoria',
    )
    readonly_fields = ('uuid', 'id')
