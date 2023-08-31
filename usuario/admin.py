from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from usuario.models import Usuario
from core.models import Coordenadoria


class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('id', 'username', 'first_name', 'email', 'coordenadoria', 'sistema', 'date_joined', )
    search_fields = ('first_name',  'email', )
    search_help_text = 'Pesquise por nome.'

    fieldsets = (('Acesso', {'fields': ('username', 'password')}), ('Informações pessoais', {'fields': ('first_name', 'email', 'coordenadoria', 'sistema', )}),
                 ('Permissões', {'fields': ('is_active', 'is_staff', )}), )
    add_fieldsets = (('Acesso', {'fields': ('username', 'password1', 'password2')}), ('Informações pessoais', {'fields': ('first_name', 'email', 'coordenadoria', 'sistema',)}),
                     ('Permissões', {'fields': ('is_active', 'is_staff', )}), )

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
