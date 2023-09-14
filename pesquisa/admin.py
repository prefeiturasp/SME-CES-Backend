from django.contrib import admin
from django.db.models import Q
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from rangefilter.filters import DateRangeFilter
from .models import Pesquisa, Resposta, Token
from core.models import Acao


@admin.register(Pesquisa)
class PesquisaAdmin(admin.ModelAdmin):
    model = Pesquisa
    list_display = ('id', 'ativa', 'sistema', 'acao', 'criado_em', 'alterado_em', )
    readonly_fields = ('uuid', 'id', 'criado_em', 'alterado_em')
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


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    model = Token
    list_display = ('uuid', 'usuario', 'pesquisa', 'respondida', 'respondida_em', 'criado_em', 'alterado_em', )
    raw_id_fields = ('usuario', 'pesquisa', )
    readonly_fields = ('pulos', 'uuid', 'id', 'criado_em', 'alterado_em', 'uuid_resposta', 'nota_resposta', 'comentario_resposta',)
    list_filter = (
        ('pesquisa__acao__sistema__nome', DropdownFilter),
        ('criado_em', DateRangeFilter),
    )

    def respondida(self, obj):
        return 'Sim' if obj.respondida else 'Não'

    def respondida_em(self, obj):
        return obj.resposta.criado_em

    def uuid_resposta(self, obj):
        return obj.resposta.uuid

    def nota_resposta(self, obj):
        return obj.resposta.nota

    def comentario_resposta(self, obj):
        return obj.resposta.comentario
