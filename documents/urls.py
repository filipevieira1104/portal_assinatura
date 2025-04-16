from django.urls import path
from . import views
from django.views.generic.edit import UpdateView
from .models import TermoResponsabilidade
from django.urls import reverse_lazy
from django.utils import timezone
from .models import ItemTermo
from django.views.generic import TemplateView

app_name = 'documents'

urlpatterns = [
    # Equipamentos
    path('equipamentos/', views.EquipamentoListView.as_view(), name='equipamento_list'),
    path('equipamentos/novo/', views.EquipamentoCreateView.as_view(), name='equipamento_create'),
    path('equipamentos/<int:pk>/', views.EquipamentoDetailView.as_view(), name='equipamento_detail'),
    path('equipamentos/<int:pk>/editar/', views.EquipamentoUpdateView.as_view(), name='equipamento_update'),
    
    # Termos
    path('termos/', views.TermoListView.as_view(), name='termo_list'),
    path('termos/novo/', views.TermoCreateView.as_view(), name='termo_create'),
    path('termos/<uuid:uuid>/', views.TermoDetailView.as_view(), name='termo_detail'),
    path('termos/<uuid:uuid>/assinar/', views.TermoSignView.as_view(), name='termo_sign'),
    path('termos/<uuid:uuid>/preview/', views.TermoPreviewView.as_view(), name='termo_preview'),
    path('termos/<uuid:uuid>/download/', views.TermoDownloadView.as_view(), name='termo_download'),
    path('termos/<uuid:uuid>/editar/', views.TermoUpdateView.as_view(), name='termo_update'),
    
    # Modelos de Documento
    path('modelos/', views.DocumentoModeloListView.as_view(), name='modelo_list'),
    path('modelos/novo/', views.DocumentoModeloCreateView.as_view(), name='modelo_create'),
    path('modelos/<int:pk>/', views.DocumentoModeloDetailView.as_view(), name='modelo_detail'),
    path('modelos/<int:pk>/editar/', views.DocumentoModeloUpdateView.as_view(), name='modelo_update'),
    path('modelos/ajuda/', TemplateView.as_view(template_name='documents/modelo_help.html'), name='modelo_help'),
] 