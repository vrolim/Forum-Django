from django.shortcuts import render, redirect, render_to_response
from django.http.response import HttpResponse,HttpResponseRedirect
from django.template import RequestContext

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import Group, User

from forum.forms import UserCreateForm, UserProfileForm, DisciplinaForm, TurmaForm, ForumForm, CursoForm, PostForm
from forum.models import *

from django.contrib import messages
from django.db.models import Q

from datetime import datetime, date

from forum.apps import solicitacoes

def index(request):
	logado = request.user.is_authenticated()
	user = None
	if(logado):
		user = User.objects.get(username=request.user)
	return render(request,'index.html',{'logado':logado,'user':user})

def home(request):
	logado = request.user.is_authenticated()
	user = User.objects.get(username=request.user)
	usuario = Usuario.objects.get(user__pk=user.id)
	grupo = str(user.groups.all()[0])

	instituicoes = Instituicao.objects.filter(usuarios__pk=usuario.id)
	cursos = Curso.objects.filter(usuarios__pk = usuario.id)

	foruns = Forum.objects.filter(Q(turma__alunos__pk=usuario.id)|Q(turma__professores__pk=usuario.id)|Q(turma__tutores__pk=usuario.id))
	turmas = Turma.objects.filter(Q(alunos__pk=usuario.id)|Q(professores__pk=usuario.id)|Q(tutores__pk=usuario.id))
	disciplinas = Disciplina.objects.filter(usuarios__pk=usuario.id)

	atividades = solicitacoes(usuario)

	return render(request,'home.html',{'grupo':grupo,'foruns':foruns,'turmas':turmas,'cursos':cursos,'instituicoes':instituicoes,'disciplinas':disciplinas,'atividades':atividades,'logado':logado})

def entrar(request):
	try:
		logado = request.user.is_authenticated()
		try:
			newuser = request.POST['username']
		except:
			newuser = None
		if(newuser):
			if(request.user!=newuser):
				logado = False
	except:
		logado = None
	if(logado):
		return redirect('/forum/home')
	if(request.method=="POST"):
		username = request.POST['username']
		try:
			password = request.POST['password'] 
		except:
			password = request.POST['password1']
		user = authenticate(username=username, password=password)
		if(user is not None):
			if user.is_active:
				login(request, user)
				return redirect('/forum/home')
			else:
				return render(request,'login.html',{'admin':True})
		else:
			return render(request,'login.html',{'errado':True})
	return render(request,'login.html')

def sair(request):
    logout(request)
    return redirect('../')

def cadastro(request):
	logado = request.user.is_authenticated()
	if(logado):
		return redirect('/forum/home')
	form = UserCreateForm()
	form_profile = UserProfileForm()
	if(request.method=='POST'):
		form = UserCreateForm(request.POST)
		form_profile = UserProfileForm(request.POST,request.FILES)
		if(form.is_valid() and form_profile.is_valid()):
			user = form.save()
			userprofile = form_profile.save(commit=False)
			userprofile.user = user
			userprofile.save()
			g = Group.objects.get(name='Aluno') 
			g.user_set.add(user)
			return entrar(request)
	return render(request, 'cadastro.html',{'form':form,'form_profile':form_profile,'logado':logado})

def novo(request,tipo):
	logado = request.user.is_authenticated()
	user = User.objects.get(username=request.user)
	usuario = Usuario.objects.get(user__pk=user.id)
	grupo = str(user.groups.all()[0])
	atividades = solicitacoes(usuario)
	turmas = Turma.objects.filter(Q(alunos__pk=usuario.id)|Q(professores__pk=usuario.id)|Q(tutores__pk=usuario.id))

	instituicao = Instituicao.objects.filter(usuarios__pk=usuario.id)
	if not(instituicao):
		messages.add_message(request, messages.WARNING, grupo+', você precisa estar associado a alguma instituição de ensino')
		return redirect('/forum/home')		

	curso = Curso.objects.filter(usuarios__pk = usuario.id)
	if(grupo!='Admin'):
		if not(curso):
			messages.add_message(request, messages.WARNING, grupo+', você precisa estar associado a algum curso!')
			return redirect('/forum/home')

	if(tipo=='disciplina'):
		form = DisciplinaForm()
		try:
			instituicao = Instituicao.objects.get(usuarios__pk=usuario.id)
			form.fields['curso'].queryset = Curso.objects.filter(instituicao=instituicao.id)
		except:
			pass				
	elif(tipo=='turma'):
		form = TurmaForm()
		form.fields['disciplina'].queryset = Disciplina.objects.filter(usuarios__pk=usuario.id)
	elif(tipo=='forum'):
		form = ForumForm()
		form.fields['turma'].queryset = Turma.objects.filter(Q(professores__pk = usuario.id) | Q(tutores__pk=usuario.id))
	elif(tipo=='curso'):
		form = CursoForm()	
		form.fields['instituicao'].queryset = Instituicao.objects.filter(usuarios__pk = usuario.id)	

	if(request.method=="POST"):
		if(tipo=='disciplina'):
			form = DisciplinaForm(request.POST)
		elif(tipo=='turma'):
			form = TurmaForm(request.POST)
		elif(tipo=='forum'):
			form = ForumForm(request.POST) 
		elif(tipo=='curso'):
			form = CursoForm(request.POST)	
		if(form.is_valid()):
			if(tipo=='disciplina'):
				f = form.save(commit=False)
				f.adm = usuario
				f.data_criacao = date.today()
				f.save()
				disciplina = Disciplina.objects.get(pk=f.id)
				disciplina.usuarios.add(usuario)
			elif(tipo=='turma'):
				f = form.save(commit=False)
				f.data_criacao = date.today()
				f.save()				
				turma = Turma.objects.get(pk=f.id)
				if(grupo=='Admin' or grupo=='Professor'):
					turma.professores.add(usuario)
				elif(grupo=='Tutor'):
					turma.tutores.add(usuario)
			elif(tipo=='forum'):
				f = form.save(commit=False)
				f.data_criacao = date.today()
				f.criador = usuario
				f.save()				
			elif(tipo=='curso'):
				f = form.save(commit=False)
				f.data_criacao = date.today()
				f.save()
				curso = Curso.objects.get(pk=f.id)
				curso.usuarios.add(usuario)
			messages.add_message(request, messages.SUCCESS, tipo.upper()+' criado com sucesso!')
			return redirect('/forum/home')
	return render(request,'novo.html',{'form':form,'grupo':grupo,'tipo':tipo,'turmas':turmas,'atividades':atividades,'logado':logado})

def listar(request,tipo):
	logado = request.user.is_authenticated()
	user = User.objects.get(username=request.user)
	grupo = str(user.groups.all()[0])
	usuario = Usuario.objects.get(user__pk=user.id)
	atividades = solicitacoes(usuario)
	turmas = Turma.objects.filter(Q(alunos__pk=usuario.id)|Q(professores__pk=usuario.id)|Q(tutores__pk=usuario.id))

	try:
		termo = request.POST['termo']
	except:
		termo = None
	if(termo):
		instituicao = Instituicao.objects.filter(Q(nome__contains=termo) | Q(sigla__contains=termo))
		curso = Curso.objects.filter(Q(nome__contains=termo) | Q(codigo_mec__contains=termo))
		disciplina = Disciplina.objects.filter(Q(nome__contains=termo) | Q(codigo__contains=termo))
		turma = Turma.objects.filter(Q(nome__contains=termo) | Q(codigo__contains=termo) | Q(descricao__contains=termo))
		forum = Forum.objects.filter(Q(titulo__contains=termo) | Q(descricao__contains=termo))
		return render(request,'listar.html',{'termo':termo,'instituicao':instituicao,'curso':curso,'disciplina':disciplina,'turma':turma,'forum':forum,'turmas':turmas,'grupo':grupo,'logado':logado})
	else:
		if(tipo=='instituicao'):
			instituicao = Instituicao.objects.all()
			return render(request,'listar.html',{'instituicao':instituicao,'grupo':grupo,'logado':logado})
		elif(tipo=='curso'):
			curso = Curso.objects.filter(instituicao__usuarios__pk=usuario.id)
			return render(request,'listar.html',{'curso':curso,'grupo':grupo,'logado':logado})
		elif(tipo=='disciplina'):
			disciplina = Disciplina.objects.filter(curso__usuarios__pk=usuario.id)
			return render(request,'listar.html',{'disciplina':disciplina,'grupo':grupo,'logado':logado})
		elif(tipo=='turma'):
			turma = Turma.objects.filter(disciplina__usuarios__pk=usuario.id)
			return render(request,'listar.html',{'turma':turma,'grupo':grupo,'logado':logado})
		elif(tipo=='forum'):
			forum = Forum.objects.filter(Q(turma__alunos__pk=usuario.id)|Q(turma__professores__pk=usuario.id)|Q(turma__tutores__pk=usuario.id))	
			return render(request,'listar.html',{'forum':forum,'grupo':grupo,'logado':logado})
		else:
			disciplina = Disciplina.objects.all()
			turma = Turma.objects.all()
			forum = Forum.objects.all()	
			curso = Curso.objects.all()
			instituicao = Instituicao.objects.all()
			return render(request,'listar.html',{'instituicao':instituicao,'curso':curso,'disciplina':disciplina,'turma':turma,'forum':forum,'turmas':turmas,'atividades':atividades,'grupo':grupo,'logado':logado})

def add(request,tipo,tipo_id):
	logado = request.user.is_authenticated()
	user = User.objects.get(username=request.user)
	grupo = str(user.groups.all()[0])	
	usuario = Usuario.objects.get(user__pk=user.id)
	try:
		solic = Solicitacao.objects.filter(Q(tipo_id=tipo_id)&Q(tipo=tipo)&Q(usuario=usuario)&Q(ativa=True))
		if(solic):
			messages.add_message(request, messages.WARNING,'Você já realizou essa solicitação anteriormente, aguarde a aceitação da sua solicitação!')
			return redirect('/forum/listar/'+tipo)
	except:
		pass
	solicitacao = Solicitacao()
	solicitacao.tipo = tipo
	solicitacao.tipo_id = tipo_id
	solicitacao.usuario = usuario
	solicitacao.data_solicitacao = datetime.now()
	solicitacao.ativa = True
	solicitacao.save()

	messages.add_message(request, messages.SUCCESS,'Sua solicitação foi enviada a administracao da '+tipo+'!')

	return redirect('/forum/listar/'+tipo)

def interacao(request,forum_id):
	logado = request.user.is_authenticated()
	user = User.objects.get(username=request.user)
	usuario = Usuario.objects.get(user__pk=user.id)
	atividades = solicitacoes(usuario)	
	turmas = Turma.objects.filter(Q(alunos__pk=usuario.id)|Q(professores__pk=usuario.id)|Q(tutores__pk=usuario.id))

	grupo = str(user.groups.all()[0])	
	form = PostForm()
	posts = Post.objects.filter(forum = forum_id)
	forum = Forum.objects.get(pk=forum_id)
	if(request.method=="POST"):
		form = PostForm(request.POST)
		if(form.is_valid()):
			f = form.save(commit=False)
			f.autor = usuario
			f.data_post = datetime.now()
			f.forum = forum
			f.save()
			return redirect('/forum/interacao/'+str(forum_id))
	return render(request,'interacao.html',{'grupo':grupo,'form':form,'posts':posts,'forum':forum,'turmas':turmas,'atividades':atividades,'logado':logado})

def painel(request):
	logado = request.user.is_authenticated()
	user = User.objects.get(username=request.user)
	usuario = Usuario.objects.get(user__pk=user.id)	
	turmas = Turma.objects.filter(Q(alunos__pk=usuario.id)|Q(professores__pk=usuario.id)|Q(tutores__pk=usuario.id))
	grupo = str(user.groups.all()[0])		
	atividades = solicitacoes(usuario)	

	return render(request,'painel.html',{'usuario':usuario,'grupo':grupo,'turmas':turmas,'atividades':atividades,'logado':logado})

def visualizacao(request,tipo,tipo_id):
	logado = request.user.is_authenticated()
	user = User.objects.get(username=request.user)
	usuario = Usuario.objects.get(user__pk=user.id)	
	turmas = Turma.objects.filter(Q(alunos__pk=usuario.id)|Q(professores__pk=usuario.id)|Q(tutores__pk=usuario.id))
	grupo = str(user.groups.all()[0])		
	atividades = solicitacoes(usuario)

	if(tipo=='instituicao'):
		instituicao = Instituicao.objects.get(pk=tipo_id)
		cursos = Curso.objects.filter(instituicao__pk=tipo_id)
		return render(request,'visualizacao.html',{'instituicao':instituicao,'cursos':cursos,'grupo':grupo,'turmas':turmas,'atividades':atividades,'logado':logado})
	elif(tipo=='curso'):
		curso = Curso.objects.get(pk=tipo_id)
		disciplinas = Disciplina.objects.filter(curso__pk=tipo_id)
		return render(request,'visualizacao.html',{'curso':curso,'disciplinas':disciplinas,'grupo':grupo,'turmas':turmas,'atividades':atividades,'logado':logado})
	elif(tipo=='disciplina'):
		disciplina = Disciplina.objects.get(pk=tipo_id)
		turmass = Turma.objects.filter(disciplina__pk=tipo_id)
		return render(request,'visualizacao.html',{'disciplina':disciplina,'turmass':turmass,'grupo':grupo,'turmas':turmas,'atividades':atividades,'logado':logado})
	elif(tipo=='turma'):
		turma = Turma.objects.get(pk=tipo_id)
		foruns = Forum.objects.filter(turma__pk=tipo_id)
		return render(request,'visualizacao.html',{'turma':turma,'foruns':foruns,'grupo':grupo,'turmas':turmas,'atividades':atividades,'logado':logado})
	elif(tipo=='forum'):
		return redirect('/forum/interacao/'+str(tipo_id))	
	else:
		messages.add_message(request, messages.WARNING,'Algum problema aconteceu, estamos trabalhando para resolver!')
		return render(request,'visualizacao.html',{'usuario':usuario,'grupo':grupo,'turmas':turmas,'atividades':atividades,'logado':logado})

def solicitacao(request, solicitacao_id,resposta):
	solic = Solicitacao.objects.get(pk=solicitacao_id)
	print(solic.ativa)
	solic.ativa = False
	solic.save()
	user_solic = Usuario.objects.get(pk=solic.usuario.id)

	if(resposta=='1'):
		if(solic.tipo=='instituicao'):
			try:
				obj = Instituicao.objects.get(Q(pk=solic.tipo_id)&Q(usuarios=user_solic.id))
				messages.add_message(request, messages.WARNING,'Esta solicitação já foi aprovada anteriormente!')
			except:
				obj = Instituicao.objects.get(pk=solic.tipo_id)
				obj.usuarios.add(user_solic)
				messages.add_message(request, messages.SUCCESS,str(solic)+' aprovada!')
		elif(solic.tipo=='curso'):
			try:
				obj = Curso.objects.get(Q(pk=solic.tipo_id)&Q(usuarios=user_solic.id))
				messages.add_message(request, messages.WARNING,'Esta solicitação já foi aprovada anteriormente!')
			except:			
				obj = Curso.objects.get(pk=solic.tipo_id)
				obj.usuarios.add(user_solic)
				messages.add_message(request, messages.SUCCESS,str(solic)+' aprovada!')
		elif(solic.tipo=='disciplina'):
			try:
				obj = Disciplina.objects.get(Q(pk=solic.tipo_id)&Q(usuarios=user_solic.id))
				messages.add_message(request, messages.WARNING,'Esta solicitação já foi aprovada anteriormente!')
			except:			
				obj = Disciplina.objects.get(pk=solic.tipo_id)
				obj.usuarios.add(user_solic)
				messages.add_message(request, messages.SUCCESS,str(solic)+' aprovada!')
		elif(solic.tipo=='turma'):
			try:
				obj = Turma.objects.get(Q(pk=solic.tipo_id)&Q(alunos=user_solic.id))
				messages.add_message(request, messages.WARNING,'Esta solicitação já foi aprovada anteriormente!')
			except:			
				obj = Turma.objects.get(pk=solic.tipo_id)
				obj.alunos.add(user_solic)
				messages.add_message(request, messages.SUCCESS,'Solicitação '+str(obj)+' aprovada!')
	else:
		messages.add_message(request, messages.SUCCESS, str(solic)+' Rejeitada!')

	return redirect('/forum/painel')