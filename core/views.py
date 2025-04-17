from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from documents.models import Equipamento, TermoResponsabilidade, DocumentoModelo

# Create your views here.

class HomeView(TemplateView):
    template_name = 'core/home.html'

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_staff:
            # Contexto para administradores
            # Contagens
            context['total_equipamentos'] = Equipamento.objects.count()
            context['total_termos'] = TermoResponsabilidade.objects.count()
            context['termos_pendentes'] = TermoResponsabilidade.objects.filter(status='PENDENTE').count()
            context['termos_assinados'] = TermoResponsabilidade.objects.filter(status='ASSINADO').count()
            
            # Listas para tabelas
            context['ultimos_termos'] = TermoResponsabilidade.objects.all().order_by('-data_envio')[:5]
            context['ultimos_equipamentos'] = Equipamento.objects.all().order_by('-data_aquisicao')[:5]
        else:
            # Contexto para colaboradores
            context['meus_equipamentos'] = Equipamento.objects.filter(usuario=user)
            context['termos_pendentes'] = TermoResponsabilidade.objects.filter(colaborador=user, status='PENDENTE')
            context['termos_assinados'] = TermoResponsabilidade.objects.filter(colaborador=user, status='ASSINADO')
            context['total_equipamentos'] = context['meus_equipamentos'].count()
            context['total_termos'] = TermoResponsabilidade.objects.filter(colaborador=user).count()
        
        return context
