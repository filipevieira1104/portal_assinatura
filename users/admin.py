from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'cpf', 'cargo', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'cargo', 'departamento')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'cpf')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Informações Pessoais'), {
            'fields': (
                'first_name', 'last_name', 'email', 'cpf', 'rg',
                'data_nascimento', 'telefone'
            )
        }),
        (_('Endereço'), {
            'fields': (
                'endereco', 'numero', 'complemento', 'bairro',
                'cidade', 'estado', 'cep'
            )
        }),
        (_('Informações Profissionais'), {
            'fields': ('cargo', 'departamento')
        }),
        (_('Permissões'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            ),
        }),
        (_('Datas importantes'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'cpf', 'email', 'first_name', 'last_name'),
        }),
    )
