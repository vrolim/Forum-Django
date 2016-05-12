from forum.models import *

from django.contrib import messages
from django.db.models import Q

from datetime import datetime, date

def solicitacoes(usuario):
	solicitacoes = Solicitacao.objects.filter(ativa=True)
	print(solicitacoes)
	atividades = []
	for solicitacao in solicitacoes:
		if(solicitacao.tipo=='instituicao'):
			instituicao = Instituicao.objects.filter(Q(pk=solicitacao.tipo_id) & Q(adm=usuario))
			if(instituicao):
				if(solicitacao not in atividades):
					atividades.append(solicitacao)
		elif(solicitacao.tipo=='curso'):
			curso = Curso.objects.filter(Q(pk=solicitacao.id) & Q(usuarios__pk=usuario.id))
			if(curso):
				for c in curso:
					for pessoa in c.usuarios.all():
						if(pessoa.groups.all()[0]=='Admin'):
							if(solicitacao not in atividades):
								atividades.append(solicitacao)
		elif(solicitacao.tipo=='disciplina'):
			disciplina = Disciplina.objects.filter(Q(pk=solicitacao.id) & Q(usuarios__pk=usuario.id))
			if(disciplina):
				for d in disciplina:
					for pessoa in c.usuarios.all():
						if(pessoa.groups.all()[0]=='Admin'):
							if(solicitacao not in atividades):
								atividades.append(solicitacao)			
		elif(solicitacao.tipo=='turma'):
			turma = Turma.objects.filter(Q(pk=solicitacao.id) & (Q(professores__pk=usuario.id)|Q(tutores__pk=usuario.id)))
			if(turma):
				if(solicitacao not in atividades):
					atividades.append(solicitacao)				
		elif(solicitacao.tipo=='forum'):
			forum - Forum.objects.filter(Q(pk=solicitacao.id) & (Q(turma__professores__pk=usuario.id)|Q(turma__tutores__pk=usuario.id)))
			if(forum):
				if(solicitacao not in atividades):
					atividades.append(solicitacao)
	return atividades	