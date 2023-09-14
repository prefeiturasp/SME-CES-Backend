from django.contrib import admin
from .models import Relatorio


@admin.register(Relatorio)
class RelatorioAdmin(admin.ModelAdmin):
    model = Relatorio
    list_display = ('id', 'coordenadoria', 'sistema', 'pesquisa', 'criado_em', 'criado_por')
    readonly_fields = ('uuid', 'id', 'criado_em', 'criado_por',)

    def sistema(self, obj):
        return obj.pesquisa.acao.sistema.nome

    def coordenadoria(self, obj):
        return obj.pesquisa.acao.sistema.coordenadoria.nome

    def save_model(self, request, obj, form, change):
        obj.criado_por = request.user
        obj.save()
