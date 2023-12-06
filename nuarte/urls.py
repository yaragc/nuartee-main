from django.urls import path
from nuarte.views import (
    index, ListarInstrumentosView, CadastrarInstrumentoView, AtualizarInstrumentoView, DeletarInstrumentoView, InstrumentoDetailView,
    ListarPerfisView, CadastrarPerfilView, AtualizarPerfilView, DeletarPerfilView,
    ListarHistoricoView, solicitar_instrumento, devolver_instrumento, administracao, listar_solicitacoes, aprovar_solicitacao, rejeitar_solicitacao, gerenciamento_instrumentos
)

app_name = 'nuarte'

urlpatterns = [
    path('', index, name='index'),
    path('listar_instrumentos/', ListarInstrumentosView.as_view(), name='listar_instrumentos'),
    path('cadastrar_instrumento/', CadastrarInstrumentoView.as_view(), name='cadastrar_instrumento'),
    path('atualizar_instrumento/<int:pk>/', AtualizarInstrumentoView.as_view(), name='atualizar_instrumento'),
    path('deletar_instrumento/<int:pk>/', DeletarInstrumentoView.as_view(), name='deletar_instrumento'),
    path('detalhes_instrumento/<int:pk>/', InstrumentoDetailView.as_view(), name='detalhes_instrumento'),

    path('listar_perfis/', ListarPerfisView.as_view(), name='listar_perfis'),
    path('cadastrar_perfil/', CadastrarPerfilView.as_view(), name='cadastrar_perfil'),
    path('atualizar_perfil/<int:pk>/', AtualizarPerfilView.as_view(), name='atualizar_perfil'),
    path('deletar_perfil/<int:pk>/', DeletarPerfilView.as_view(), name='deletar_perfil'),

    path('listar_historico/', ListarHistoricoView.as_view(), name='listar_historico'),
    path('solicitar_instrumento/', solicitar_instrumento, name='solicitar_instrumento'),
    path('devolver_instrumento/<int:instrumento_id>/', devolver_instrumento, name='devolver_instrumento'),
    path('listar_solicitacoes/', listar_solicitacoes, name='listar_solicitacoes'),
    path('aprovar_solicitacao/<int:historico_id>/', aprovar_solicitacao, name='aprovar_solicitacao'),
    path('rejeitar_solicitacao/<int:historico_id>/', rejeitar_solicitacao, name='rejeitar_solicitacao'),
    path('administracao/', administracao, name='administracao'),
    path('gerenciamento_instrumentos/', gerenciamento_instrumentos, name='gerenciamento_instrumentos'),
]
