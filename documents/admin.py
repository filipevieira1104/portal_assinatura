from django.contrib import admin
from .models import Equipamento, DocumentoModelo, TermoResponsabilidade, ItemTermo

class ItemTermoInline(admin.TabularInline):
    model = ItemTermo
    extra = 1
    fields = ('equipamento', 'data_entrega', 'estado_entrega', 'data_devolucao', 'estado_devolucao')

@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'marca', 'modelo', 'numero_serie', 'valor', 'status')
    list_filter = ('tipo', 'status', 'marca')
    search_fields = ('numero_serie', 'marca', 'modelo', 'descricao')
    ordering = ('tipo', 'marca', 'modelo')

@admin.register(DocumentoModelo)
class DocumentoModeloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'versao', 'ativo', 'data_modificacao')
    list_filter = ('ativo', 'data_criacao')
    search_fields = ('titulo', 'conteudo')
    ordering = ('-data_modificacao',)

@admin.register(TermoResponsabilidade)
class TermoResponsabilidadeAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'colaborador', 'status', 'data_envio', 'data_assinatura')
    list_filter = ('status', 'data_envio', 'data_assinatura')
    search_fields = ('uuid', 'colaborador__username', 'colaborador__first_name', 'colaborador__last_name')
    ordering = ('-data_envio',)
    inlines = [ItemTermoInline]
    readonly_fields = ('uuid', 'data_envio', 'data_assinatura', 'ip_assinatura', 'hash_assinatura')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('colaborador', 'modelo')
