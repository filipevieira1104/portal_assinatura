from django.contrib import admin
from .models import Equipamento, DocumentoModelo, TermoResponsabilidade, ItemTermo

class ItemTermoInline(admin.TabularInline):
    model = ItemTermo
    extra = 1
    fields = ('equipamento', 'data_entrega', 'estado_entrega', 'data_devolucao', 'estado_devolucao')

@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'marca', 'modelo', 'numero_serie', 'status', 'usuario')
    list_filter = ('tipo', 'status')
    search_fields = ('numero_serie', 'marca', 'modelo')

@admin.register(DocumentoModelo)
class DocumentoModeloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'versao', 'ativo', 'data_criacao', 'data_modificacao', 'tem_arquivo_word')
    list_filter = ('ativo',)
    search_fields = ('titulo',)
    readonly_fields = ('data_criacao', 'data_modificacao')
    
    def tem_arquivo_word(self, obj):
        return bool(obj.arquivo_word)
    tem_arquivo_word.short_description = 'Arquivo Word'
    tem_arquivo_word.boolean = True

@admin.register(TermoResponsabilidade)
class TermoResponsabilidadeAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'colaborador', 'modelo', 'status', 'data_envio', 'data_assinatura')
    list_filter = ('status',)
    search_fields = ('uuid', 'colaborador__username', 'colaborador__first_name', 'colaborador__last_name')
    inlines = [ItemTermoInline]
    readonly_fields = ('uuid', 'data_envio', 'data_assinatura', 'ip_assinatura', 'hash_assinatura')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('colaborador', 'modelo')
