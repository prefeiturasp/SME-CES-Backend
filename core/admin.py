from django.contrib import admin
from django.db.models import Q
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from rangefilter.filters import DateRangeFilter
from .models import Coordenadoria, Sistema, Acao


@admin.register(Coordenadoria)
class CoordenadoriaAdmin(admin.ModelAdmin):
    model = Coordenadoria
    list_display = ('nome', 'alterado_em', )


@admin.register(Acao)
class AcaoAdmin(admin.ModelAdmin):

    list_display = ('nome', 'sistema', 'rota',  'modulo', 'submodulo', 'alterado_em', )
    search_fields = ('uuid', 'nome', 'sistema__nome')
    readonly_fields = ('uuid', 'id', 'criado_em', 'alterado_em')
    raw_id_fields = ('sistema', )

    list_filter = (
        ('sistema__nome', DropdownFilter),
        ('criado_em', DateRangeFilter),
    )

    def get_queryset(self, request):
        user = request.user

        if user.is_po:
            return Acao.objects.filter(sistema=user.sistema)
        if user.is_coordenador:
            return Acao.objects.filter(sistema__coordenadoria=user.coordenadoria)
        return Acao.objects.all()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user = request.user

        if user.is_po:
            if db_field.name == "sistema":
                kwargs["queryset"] = Sistema.objects.filter(id=user.sistema.id)
        if user.is_coordenador:
            if db_field.name == "sistema":
                kwargs["queryset"] = Sistema.objects.filter(coordenadoria=user.coordenadoria)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Sistema)
class SistemaAdmin(admin.ModelAdmin):

    list_display = ('nome', 'coordenadoria', 'alterado_em', )
    search_fields = ('uuid', 'nome',)
    list_filter = (
        'coordenadoria',
    )
    readonly_fields = ('uuid', 'id', 'criado_em', 'alterado_em')

    list_filter = (
        ('coordenadoria__nome', DropdownFilter),
        ('criado_em', DateRangeFilter),
    )

    def get_queryset(self, request):
        user = request.user

        if user.is_po:
            return Sistema.objects.filter(id=user.sistema.id)
        if user.is_coordenador:
            return Sistema.objects.filter(coordenadoria__in=user.coordenadoria__in)
        return Sistema.objects.all()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user = request.user

        if user.is_coordenador:
            if db_field.name == "coordenadoria":
                kwargs["queryset"] = Coordenadoria.objects.filter(usuarios_coordenadoria__in=[user])

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
