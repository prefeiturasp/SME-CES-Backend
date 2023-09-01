from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy
from usuario.models import Usuario
from core.models import Coordenadoria


def reenviar_email_redefinicao_senha(modeladmin, request, queryset):
    for item in queryset:
        item.enviar_email_redefinicao_senha()


class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('id', 'email', 'first_name', 'coordenadoria', 'sistema', 'date_joined', )
    search_fields = ('first_name',  'email', )
    search_help_text = 'Pesquise por nome.'

    fieldsets = (('Acesso', {'fields': ('username', 'password')}), ('Informações pessoais', {'fields': ('first_name', 'coordenadoria', 'sistema', )}),
                 ('Permissões', {'fields': ('is_active', 'is_staff', )}), )
    add_fieldsets = (('Acesso', {'fields': ('username', 'password1', 'password2')}),
                     ('', {'fields': ('first_name', 'coordenadoria', 'sistema',)}),)

    actions = [
        reenviar_email_redefinicao_senha,
    ]

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'username':
            kwargs['label'] = 'Email'
        return super().formfield_for_dbfield(db_field, **kwargs)

    def get_queryset(self, request):
        user = request.user

        if user.is_coordenador:
            return Usuario.objects.filter(coordenadoria=user.coordenadoria)
        return Usuario.objects.all()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user = request.user

        if user.is_coordenador:
            if db_field.name == "coordenadoria":
                kwargs["queryset"] = Coordenadoria.objects.filter(usuarios_coordenadoria__in=[user])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Usuario, UsuarioAdmin)
admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
