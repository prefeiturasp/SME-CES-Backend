from import_export import resources
from django.contrib import admin
from django.db.models import Q
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from rangefilter.filters import DateRangeFilter
from import_export import fields
from import_export.admin import ImportExportModelAdmin

from .models import Pesquisa, Token, Resposta
from core.models import Acao


@admin.register(Pesquisa)
class PesquisaAdmin(admin.ModelAdmin):
    model = Pesquisa
    list_display = ('id', 'ativa', 'sistema', 'acao', 'criado_em', 'alterado_em', )
    readonly_fields = ('anonima', 'uuid', 'id', 'criado_em', 'alterado_em')
    search_fields = ('uuid', 'nome', 'acao__sistema__nome', 'acao__sistema_coordenadoria__nome')
    search_help_text = 'Pesquise por uuid, nome, sistema ou coordenadoria.'
    raw_id_fields = ('acao', )

    list_filter = (
        ('acao__sistema__nome', DropdownFilter),
        ('criado_em', DateRangeFilter),
        'ativa'
    )

    def sistema(self, obj):
        return obj.acao.sistema.nome

    def get_queryset(self, request):
        user = request.user

        if user.is_po:
            return Pesquisa.objects.filter(acao__sistema=user.sistema.id)
        if user.is_coordenador:
            return Pesquisa.objects.filter(acao__sistema__coordenadoria=user.coordenadoria)

        return Pesquisa.objects.all()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user = request.user

        if user.is_coordenador:
            if db_field.name == "acao":
                kwargs["queryset"] = Acao.objects.filter(sistema__coordenadoria=user.coordenadoria)
        if user.is_po:
            if db_field.name == "acao":
                kwargs["queryset"] = Acao.objects.filter(sistema=user.sistema)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class RespostaInline(admin.TabularInline):
    extra = 0
    model = Resposta
    readonly_fields = ('uuid', 'nota', 'comentario', )


class TokenResource(resources.ModelResource):
    coordenadoria = fields.Field()
    sistema = fields.Field()
    nota = fields.Field()
    comentario = fields.Field()
    criado_em = fields.Field()
    alterado_em = fields.Field()

    class Meta:
        model = Token
        fields = ('coordenadoria', 'sistema', 'pesquisa', 'usuario', 'nota', 'comentario', 'pulos', 'criado_em', 'alterado_em', )
        export_order = ('coordenadoria', 'sistema', 'pesquisa', 'usuario', 'nota', 'comentario', 'pulos', 'criado_em', 'alterado_em', )

    def dehydrate_usuario(self, obj):
        return obj.usuario.nome

    def dehydrate_coordenadoria(self, obj):
        return obj.pesquisa.acao.sistema.coordenadoria.nome

    def dehydrate_sistema(self, obj):
        return obj.pesquisa.acao.sistema.nome

    def dehydrate_pesquisa(self, obj):
        return obj.pesquisa.__str__()

    def dehydrate_nota(self, obj):
        try:
            return obj.resposta.nota
        except Exception:
            return '-'

    def dehydrate_comentario(self, obj):
        try:
            return obj.resposta.comentario
        except Exception:
            return '-'

    def dehydrate_criado_em(self, obj):
        try:
            return obj.resposta.criado_em
        except Exception:
            return '-'

    def dehydrate_alterado_em(self, obj):
        try:
            return obj.resposta.alterado_em
        except Exception:
            return '-'

@admin.register(Token)
class TokenAdmin(ImportExportModelAdmin):
    resource_class = TokenResource
    model = Token
    list_display = ('uuid', 'usuario', 'pesquisa', 'respondida', 'respondida_em', 'criado_em', 'alterado_em', )
    raw_id_fields = ('usuario', 'pesquisa', )
    readonly_fields = ('pulos', 'uuid', 'id', 'criado_em', 'alterado_em', )
    list_filter = (
        ('pesquisa__acao__sistema__coordenadoria__nome', DropdownFilter),
        ('pesquisa__acao__sistema__nome', DropdownFilter),
        ('pesquisa__acao__nome', DropdownFilter),
        ('criado_em', DateRangeFilter)
    )

    inlines = [RespostaInline]

    def respondida(self, obj):
        return 'Sim' if obj.respondida else 'Não'

    def respondida_em(self, obj):
        return obj.resposta.criado_em

    def get_queryset(self, request):
        user = request.user

        if user.is_po:
            return Token.objects.filter(pesquisa__acao__sistema=user.sistema.id)
        if user.is_coordenador:
            return Token.objects.filter(pesquisa__acao__sistema__coordenadoria=user.coordenadoria)

        return Token.objects.all()
