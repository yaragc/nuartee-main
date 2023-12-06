from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Instrumento, Historico, Perfil

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (PerfilInline, )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Instrumento)
class InstrumentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'disponivel')
    list_filter = ('disponivel',)
    search_fields = ('nome', 'descricao')

@admin.register(Historico)
class HistoricoAdmin(admin.ModelAdmin):
    list_display = ('data_operacao', 'usuario', 'instrumento', 'operacao')
    list_filter = ('usuario', 'instrumento', 'operacao')
    search_fields = ('usuario__username', 'instrumento__nome', 'operacao')

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_usuario')
    list_filter = ('tipo_usuario',)
    search_fields = ('usuario__username', 'tipo_usuario')
