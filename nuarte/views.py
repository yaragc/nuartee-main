from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Instrumento, Historico, Perfil
from .forms import InstrumentoForm, PerfilForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator

# Função de teste para verificar se o usuário é um administrador
def is_admin(user):
    return user.is_authenticated and user.groups.filter(name='Administradores').exists()

def admin_group_required(view_func):
    actual_decorator = user_passes_test(is_admin)
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

# Seção do decorador admin_group_required
def admin_group_required(view_func):
    actual_decorator = user_passes_test(is_admin)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.groups.filter(name='Administradores').exists():
            return view_func(request, *args, **kwargs)
        else:
            return render(request, '403.html') 
    return _wrapped_view

# Seção do decorador admin_group_required
def admin_group_required(view_func):
    actual_decorator = user_passes_test(is_admin)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.groups.filter(name='Administradores').exists():
            return view_func(request, *args, **kwargs)
        else:
            return render(request, '403.html') 
    return _wrapped_view

class ListarInstrumentosView(ListView):
    model = Instrumento
    template_name = 'nuarte/listar_instrumentos.html'
    context_object_name = 'instrumentos'
    paginate_by = 6

@method_decorator(user_passes_test(is_admin), name='dispatch')
class CadastrarInstrumentoView(SuccessMessageMixin, CreateView):
    model = Instrumento
    form_class = InstrumentoForm
    template_name = 'nuarte/cadastrar_instrumento.html'
    success_url = reverse_lazy('nuarte:listar_instrumentos')
    success_message = 'Instrumento cadastrado com sucesso!'

@method_decorator(user_passes_test(is_admin), name='dispatch')
class AtualizarInstrumentoView(SuccessMessageMixin, UpdateView):
    model = Instrumento
    form_class = InstrumentoForm
    template_name = 'nuarte/editar_instrumento.html'
    success_url = reverse_lazy('nuarte:listar_instrumentos')
    success_message = 'Instrumento atualizado com sucesso!'

@method_decorator(user_passes_test(is_admin), name='dispatch')
class DeletarInstrumentoView(SuccessMessageMixin, DeleteView):
    model = Instrumento
    template_name = 'nuarte/deletar_instrumento.html'
    success_url = reverse_lazy('nuarte:listar_instrumentos')
    success_message = 'Instrumento deletado com sucesso!'

class ListarPerfisView(ListView):
    model = Perfil
    template_name = 'nuarte/listar_perfis.html'
    context_object_name = 'perfis'

class CadastrarPerfilView(SuccessMessageMixin, CreateView):
    model = Perfil
    form_class = PerfilForm
    template_name = 'nuarte/cadastrar_perfil.html'
    success_url = reverse_lazy('nuarte:listar_perfis')
    success_message = 'Perfil cadastrado com sucesso!'


class AtualizarPerfilView(SuccessMessageMixin, UpdateView):
    model = Perfil
    form_class = PerfilForm
    template_name = 'nuarte/atualizar_perfil.html'
    success_url = reverse_lazy('nuarte:listar_perfis')
    success_message = 'Perfil atualizado com sucesso!'

class DeletarPerfilView(SuccessMessageMixin, DeleteView):
    model = Perfil
    template_name = 'nuarte/deletar_perfil.html'
    success_url = reverse_lazy('nuarte:listar_perfis')
    success_message = 'Perfil deletado com sucesso!'

class ListarHistoricoView(ListView):
    template_name = 'nuarte/listar_historico.html'

    def get(self, request, *args, **kwargs):
        historico = Historico.objects.all()
        return render(request, self.template_name, {'historico': historico})

    paginate_by = 8

class InstrumentoDetailView(DetailView):
    model = Instrumento
    template_name = 'nuarte/detalhes_instrumento.html'
    context_object_name = 'instrumento'

from django.shortcuts import render, redirect
from .models import Instrumento, Historico

def solicitar_instrumento(request):
    if request.method == 'POST':
        instrumento_id = request.POST.get('instrumento')
        instrumento = Instrumento.objects.get(pk=instrumento_id)

        Historico.objects.create(
            usuario=request.user,
            instrumento=instrumento,
            operacao='Solicitação de instrumento'
        )
 
        messages.success(request, 'Instrumento solicitado com sucesso!')
        return redirect('nuarte:listar_instrumentos')

    instrumentos_disponiveis = Instrumento.objects.filter(disponivel=True)
    return render(request, 'nuarte/solicitar_instrumento.html', {'instrumentos_disponiveis': instrumentos_disponiveis})

def devolver_instrumento(request, instrumento_id):
    try:
        instrumento = Instrumento.objects.get(pk=instrumento_id)

        if not instrumento.disponivel:
            instrumento.disponivel = True
            instrumento.save()

            Historico.objects.create(
                usuario=request.user,
                instrumento=instrumento,
                operacao='Devolução de instrumento'
            )

            messages.success(request, 'Instrumento devolvido com sucesso!')
        else:
            messages.error(request, 'Este instrumento já está disponível.')

        return redirect('nuarte:listar_instrumentos')

    except Instrumento.DoesNotExist:
        messages.error(request, 'Instrumento não encontrado.')
        return redirect('nuarte:listar_instrumentos')

def listar_solicitacoes(request):
    # Obtém todas as solicitações pendentes
    solicitacoes_pendentes = Historico.objects.filter(aprovado=False)

    return render(request, 'nuarte/listar_solicitacoes.html', {'solicitacoes_pendentes': solicitacoes_pendentes})

def aprovar_solicitacao(request, historico_id):
    historico = get_object_or_404(Historico, pk=historico_id)

    # Atualiza o status para aprovado e a disponibilidade do instrumento
    historico.aprovado = True
    historico.instrumento.disponivel = False  # Instrumento indisponível após aprovação
    historico.save()
    historico.instrumento.save()

    messages.success(request, 'Solicitação aprovada com sucesso!')
    return redirect('nuarte:listar_solicitacoes')

def rejeitar_solicitacao(request, historico_id):
    historico = get_object_or_404(Historico, pk=historico_id)

    # Atualiza o status para rejeitado
    historico.aprovado = False
    historico.save()

    messages.success(request, 'Solicitação rejeitada com sucesso!')
    return redirect('nuarte:listar_solicitacoes')

@admin_group_required
def administracao(request):
    return render(request, 'nuarte/administracao.html')

def index(request):
    return render(request, 'nuarte/index.html')

def gerenciamento_instrumentos(request):
    instrumentos = Instrumento.objects.all()
    return render(request, 'nuarte/gerenciamento_instrumentos.html', {'instrumentos': instrumentos})