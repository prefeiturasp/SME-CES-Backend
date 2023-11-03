from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rest_framework.authtoken.models import TokenProxy
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from usuario.models import Usuario
from core.models import Coordenadoria


def reenviar_email_redefinicao_senha(modeladmin, request, queryset):
    for item in queryset:
        item.enviar_email_redefinicao_senha()


class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('id', 'nome', 'email', 'coordenadoria', 'sistema', 'date_joined', )
    search_fields = ('nome',  'email', )
    list_filter = (
        ('coordenadoria__nome', DropdownFilter),
        ('sistema__nome', DropdownFilter),
        'is_staff',
        'is_superuser',
        'is_active',
        'groups',
    )
    search_help_text = 'Pesquise por nome.'
    fieldsets = (('Acesso', {'fields': ('username', 'password')}), ('Informações pessoais', {'fields': ('nome', 'email', 'coordenadoria', 'sistema', )}),
                 ('Permissões', {'fields': ('is_active', 'is_staff', 'groups',)}), ('API', {'fields': ('auth_token', )}))
    add_fieldsets = (('Acesso', {'fields': ('username', 'password1', 'password2')}),
                     ('', {'fields': ('nome', 'email', 'coordenadoria', 'sistema',)}), ('Permissões', {'fields': ('is_active', 'is_staff', 'groups', )}),)
    readonly_fields = ('auth_token', )
    actions = [
        reenviar_email_redefinicao_senha,
    ]

    def formfield_for_dbfield(self, db_field, **kwargs):
        return super().formfield_for_dbfield(db_field, **kwargs)

    def get_queryset(self, request):
        user = request.user

        if user.is_coordenador:
            return Usuario.objects.filter(coordenadoria__isnull=False,
                                          coordenadoria=user.coordenadoria)
        return Usuario.objects.all()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user = request.user

        if user.is_coordenador:
            if db_field.name == "coordenadoria":
                kwargs["queryset"] = Coordenadoria.objects.filter(usuarios_coordenadoria__in=[user])
            if db_field.name == "sistema":
                kwargs["queryset"] = user.coordenadoria.sistemas
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Usuario, UsuarioAdmin)
admin.site.unregister(TokenProxy)
