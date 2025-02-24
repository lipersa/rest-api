from ninja import Router
from .schemas import AlunosSchema, ProgressoAlunoSchema, AulaRealizadaSchema
from .models import Alunos, AulasConcluidas
from ninja.errors import HttpError
from .graduacao import *
from typing import List

treino_router = Router()

@treino_router.post('',response={200: AlunosSchema})
def criar_aluno(request,aluno_schemas:AlunosSchema):
    nome = aluno_schemas.dict()['nome']
    email = aluno_schemas.dict()['email']
    faixa = aluno_schemas.dict()['faixa']
    data_nascimento = aluno_schemas.dict()['data_nascimento']

    if Alunos.objects.filter(email=email).exists():
        raise HttpError(400, 'Email já cadastrado')
    aluno = Alunos(nome=nome,
                   email=email,
                   faixa=faixa,
                   data_nascimento=data_nascimento)
    
    aluno.save()

    return aluno

@treino_router.get('/alunos/', response=List[AlunosSchema])
def listar_alunos(request):
    alunos = Alunos.objects.all()
    return alunos

@treino_router.get('/progresso_aluno/', response={200: ProgressoAlunoSchema})
def progresso_aluno(request, email_aluno: str):
    aluno = Alunos.objects.get(email=email_aluno)
    faixa_atual = aluno.get_faixa_display()
    n = order_belt.get(faixa_atual, 0 )
    aulas_necessarias_para_proxima_faixa = calculate_lesson_to_upgrade(n)
    total_aulas_concluidas_faixa = AulasConcluidas.objects.filter(aluno=aluno, faixa_atual=aluno.faixa).count()
    aulas_faltantes = aulas_necessarias_para_proxima_faixa - total_aulas_concluidas_faixa

    return {
        "email": aluno.email,
        "nome": aluno.nome,
        "faixa": faixa_atual,
        "total_aulas": total_aulas_concluidas_faixa,
        "taulas_necessarias_para_proxima_faixa": aulas_faltantes,
    }
@treino_router.post('/aula_realizada/', response={200: str})
def aula_realizada(request, aula_realizada: AulaRealizadaSchema):
    return 'teste'
    