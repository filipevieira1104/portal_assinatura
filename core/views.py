from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

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
            context['total_equipamentos'] = user.equipamentos.count()
            context['total_termos'] = user.termos_responsabilidade.count()
            context['termos_pendentes'] = user.termos_responsabilidade.filter(status='PENDENTE').count()
            context['termos_assinados'] = user.termos_responsabilidade.filter(status='ASSINADO').count()
        else:
            # Contexto para colaboradores
            context['meus_equipamentos'] = user.equipamentos.all()
            context['meus_termos'] = user.termos_responsabilidade.all()
            context['termos_pendentes'] = user.termos_responsabilidade.filter(status='PENDENTE')
        
        return context
