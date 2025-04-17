from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import User
from django.contrib.auth import get_user_model
from documents.models import TermoResponsabilidade, Equipamento
from django.contrib import messages
from django.utils.safestring import mark_safe
from .forms import UserRegisterForm, ColaboradorAdminForm
from django import forms
import uuid

User = get_user_model()

# Create your views here.

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user'
    
    def get_object(self):
        return self.request.user

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/profile_form.html'
    fields = ['first_name', 'last_name', 'email', 'telefone', 'endereco', 'numero',
              'complemento', 'bairro', 'cidade', 'estado', 'cep']
    success_url = reverse_lazy('users:profile')
    
    def get_object(self):
        return self.request.user

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class UserListView(StaffRequiredMixin, ListView):
    model = User
    template_name = 'users/colaborador_list.html'
    context_object_name = 'users'
    ordering = ['first_name', 'last_name']

class UserDetailView(StaffRequiredMixin, DetailView):
    model = User
    template_name = 'users/colaborador_detail.html'
    context_object_name = 'user'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['termos'] = TermoResponsabilidade.objects.filter(colaborador=user)
        return context

class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        form.instance.is_active = False
        messages.success(self.request, 'Sua conta foi criada! Aguarde aprovação do administrador.')
        return super().form_valid(form)

class ColaboradorListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/colaborador_list.html'
    context_object_name = 'colaboradores'
    
    def get_queryset(self):
        # Exibir apenas usuários que não são superusuários
        return User.objects.filter(is_superuser=False).order_by('first_name', 'last_name')

class ColaboradorCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = ColaboradorAdminForm
    template_name = 'users/colaborador_form.html'
    success_url = reverse_lazy('users:colaborador_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Obter a senha gerada aleatoriamente
        password = getattr(form.instance, 'random_password', None)
        
        # Exibir mensagem com a senha gerada usando mark_safe para permitir HTML
        if password:
            messages.success(
                self.request, 
                mark_safe(f"Colaborador cadastrado com sucesso! A senha gerada é: <strong>{password}</strong>")
            )
        else:
            messages.success(self.request, "Colaborador cadastrado com sucesso!")
        
        return response

class ColaboradorUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ColaboradorAdminForm
    template_name = 'users/colaborador_form.html'
    success_url = reverse_lazy('users:colaborador_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Colaborador atualizado com sucesso!")
        return response

class ColaboradorDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/colaborador_detail.html'
    context_object_name = 'colaborador'

class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user_profile'
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['termos'] = TermoResponsabilidade.objects.filter(colaborador=user)
        context['equipamentos'] = Equipamento.objects.filter(termos__colaborador=user).distinct()
        return context

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/profile_update.html'
    fields = ['first_name', 'last_name', 'email', 'telefone']
    success_url = reverse_lazy('users:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Perfil atualizado com sucesso!')
        return super().form_valid(form)


