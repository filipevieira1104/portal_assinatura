from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from documents.models import Equipamento
from django.utils import timezone
from django.urls import reverse_lazy

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # Adicionar URLs para alteração de senha
    path('alterar-senha/', auth_views.PasswordChangeView.as_view(
        template_name='users/password_change.html',
        success_url=reverse_lazy('users:password_change_done')
    ), name='password_change'),
    path('alterar-senha/concluido/', auth_views.PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'
    ), name='password_change_done'),
    
    # Colaboradores (usuários)
    path('colaboradores/', views.UserListView.as_view(), name='colaborador_list'),
    path('colaboradores/novo/', views.ColaboradorCreateView.as_view(), name='colaborador_create'),
    path('colaboradores/<int:pk>/', views.UserDetailView.as_view(), name='colaborador_detail'),
    path('colaboradores/<int:pk>/editar/', views.ColaboradorUpdateView.as_view(), name='colaborador_update'),
    
    # Perfil
    path('perfil/', views.UserProfileView.as_view(), name='profile'),
    path('perfil/editar/', views.UserUpdateView.as_view(), name='profile_update'),
] 