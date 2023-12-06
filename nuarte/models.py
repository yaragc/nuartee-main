from django.db import models
from django.contrib.auth.models import User


class Historico(models.Model):
    OPERACAO_CHOICES = [
        ('S', 'Solicitação de instrumento'),
        ('D', 'Devolução de instrumento'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    instrumento = models.ForeignKey('Instrumento', on_delete=models.CASCADE)
    operacao = models.CharField(max_length=1, choices=OPERACAO_CHOICES)
    data_operacao = models.DateTimeField(auto_now_add=True)
    devolucao = models.DateTimeField(null=True, blank=True)
    
    # Adicione o campo aprovado
    aprovado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario.username} - {self.instrumento.nome}"

class Instrumento(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    disponivel = models.BooleanField(default=True)
    imagem = models.ImageField(upload_to='instrumentos/', null=True, blank=True)

    def __str__(self):
        return self.nome


class Perfil(models.Model):
    USUARIO_CHOICES = [
        ('ADM', 'Administrador'),
        ('PROF', 'Professor'),
        ('ALUNO', 'Aluno'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=5, choices=USUARIO_CHOICES)

    def __str__(self):
        return f"{self.usuario.username} - {self.tipo_usuario}"


    

    
    