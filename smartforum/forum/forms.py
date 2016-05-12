from django import forms
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from forum.models import *

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True,label="Primeiro nome")
    last_name = forms.CharField(required=True,label="Sobrenome")

    class Meta:
        model = User
        fields = ("username","first_name","last_name","email", "password1", "password2")

class UserProfileForm(ModelForm):
	cpf = forms.CharField(required=True)
	pais = forms.CharField(required=True)
	estado = forms.CharField(required=True)
	descricao = forms.CharField(widget=forms.Textarea,label="Descrição",required=False)

	class Meta:
		model = Usuario
		exclude = ['user']

class DisciplinaForm(ModelForm):
	class Meta:
		model = Disciplina
		exclude = ['usuarios','adm','data_criacao']

	def __init__(self, *args, **kwargs):
		super(DisciplinaForm, self).__init__(*args, **kwargs)

		self.fields["curso"].widget = CheckboxSelectMultiple()
		

class TurmaForm(ModelForm):
	descricao = forms.CharField(widget=forms.Textarea,label="Descrição")

	class Meta:
		model = Turma
		exclude = ['data_criacao','alunos','tutores','professores']


class ForumForm(ModelForm):
	descricao = forms.CharField(widget=forms.Textarea,label="Descrição")	

	class Meta:
		model = Forum
		exclude = ['data_criacao','criador']

class CursoForm(ModelForm):
	
	class Meta:
		model = Curso
		exclude = ['data_criacao','usuarios']
	
class PostForm(ModelForm):
	texto = forms.CharField(widget=forms.Textarea,label="",required=False)
	class Meta:
		model = Post
		exclude = ['forum','autor','data_post','pai']