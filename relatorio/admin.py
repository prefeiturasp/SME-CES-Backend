from django.contrib import admin
from django.db.models import Q
from .models import Relatorio
from core.models import Coordenadoria, Sistema
from pesquisa.models import Pesquisa


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

    def get_queryset(self, request):
        user = request.user

        if user.is_po:
            return Relatorio.objects.filter(
                Q(sistema=user.sistema) |
                Q(pesquisa__acao__sistema=user.sistema)
            )
        if user.is_coordenador:
            return Relatorio.objects.filter(
                Q(pesquisa__acao__sistema__coordenadoria=user.coordenadoria) |
                Q(sistema__coordenadoria=user.coordenadoria) |
                Q(coordenadoria=user.coordenadoria)
            )

        return Relatorio.objects.all()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user = request.user

        if user.is_coordenador:
            if db_field.name == "sistema":
                kwargs["queryset"] = user.coordenadoria.sistemas
            if db_field.name == "coordenadoria":
                kwargs["queryset"] = Coordenadoria.objects.filter(pk=user.coordenadoria.pk)
            if db_field.name == "pesquisa":
                kwargs["queryset"] = Pesquisa.objects.filter(acao__sistema__coordenadoria=user.coordenadoria)
        if user.is_po:
            if db_field.name == "sistema":
                kwargs["queryset"] = Sistema.objects.filter(pk=user.sistema.pk)
            if db_field.name == "coordenadoria":
                kwargs["queryset"] = Coordenadoria.objects.none()
            if db_field.name == "pesquisa":
                kwargs["queryset"] = Pesquisa.objects.filter(acao__sistema=user.sistema)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
