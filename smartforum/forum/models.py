from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	cpf = models.CharField(max_length=14,blank=True,null=True,unique=True)
	pais = models.CharField(max_length=30,blank=True,null=True)
	estado = models.CharField(max_length=30,blank=True,null=True)
	cidade = models.CharField(max_length=40,blank=True,null=True)
	foto = models.FileField(upload_to='pics', null=True, blank = True, verbose_name='foto')
	descricao = models.CharField(max_length=500,blank=True,null=True)

	def __str__(self):
		return self.user.username

class Instituicao(models.Model):
	nome = models.CharField(max_length=200,blank=False,null=False)
	sigla = models.CharField(max_length=10,blank=True,null=True)
	cnpj = models.CharField(max_length=20,blank=False,null=False)
	endereco = models.CharField(max_length=500,blank=True,null=True)
	telefone = models.CharField(max_length=20,blank=True,null=True)
	email = models.EmailField(max_length=100,blank=True,null=True)
	usuarios = models.ManyToManyField(Usuario,blank=True,related_name='usuarios_instituicao')
	adm = models.ForeignKey(Usuario,blank=True,null=True, related_name='adm') 
	data_criacao = models.DateField(auto_now=False,null=False)

	def __str__(self):
		return str(self.sigla)+' - '+str(self.nome)	

class Curso(models.Model):
	nome = models.CharField(max_length=200,blank=False,null=False)
	codigo_mec = models.CharField(max_length=20,blank=False,null=False)
	instituicao = models.ForeignKey(Instituicao,blank=True,null=True)
	usuarios = models.ManyToManyField(Usuario,blank=True)
	data_criacao = models.DateField(auto_now=False,null=False)

	def __str__(self):
		return str(self.codigo_mec)+' - '+str(self.nome)

class Disciplina(models.Model):
	nome = models.CharField(max_length=200,blank=False,null=False)
	codigo = models.CharField(max_length=20,blank=False,null=False)
	curso = models.ManyToManyField(Curso,related_name='curso',blank=True)
	usuarios = models.ManyToManyField(Usuario,related_name='usuarios',blank=True)
	adm = models.ForeignKey(Usuario,blank=True,null=True)
	data_criacao = models.DateField(auto_now=False,null=False)

	def __str__(self):
		return str(self.codigo)+' - '+str(self.nome)

class Turma(models.Model):
	nome = models.CharField(max_length=200,blank=False,null=False)
	codigo = models.CharField(max_length=20,blank=False,null=False)
	descricao = models.CharField(max_length=2000,blank=True,null=True)
	alunos = models.ManyToManyField(Usuario,related_name='alunos',blank=True)
	professores = models.ManyToManyField(Usuario,related_name='professores',blank=True)
	tutores = models.ManyToManyField(Usuario,related_name='tutores',blank=True)
	disciplina = models.ForeignKey(Disciplina,blank=True,null=True)
	data_criacao = models.DateField(auto_now=False,null=False)

	def __str__(self):
		return str(self.codigo)+' - '+str(self.nome)

class Arquivo(models.Model):
	TIPOS = (
		('aula', 'Aula'),
		('exercicio','Exercício'),
		('planilha', 'Planilha'),
		('apoio', 'Material de apoio'),
		('referencia', 'Referência'),
    )
	nome = models.CharField(max_length=200,blank=False,null=False)
	arquivo = models.FileField(upload_to='documents', null=True, blank = True)
	tipo = models.CharField(max_length=11, choices=TIPOS, null=False) 
	descricao = models.CharField(max_length=500,blank=True,null=True)
	turma = models.ForeignKey(Turma,blank=True,null=True)
	data_upload = models.DateTimeField(auto_now=False,null=False)

	def __str__(self):
		return str(self.tipo)+' - '+str(self.nome)	

class Forum(models.Model):
	titulo = models.CharField(max_length=500,blank=False,null=False)
	descricao = models.CharField(max_length=2000,blank=True,null=True)
	turma = models.ForeignKey(Turma,blank=True,null=True)
	data_criacao = models.DateField(auto_now=False,null=False)
	criador = models.ForeignKey(Usuario,blank=True,null=True)

	def __str__(self):
		return str(self.turma.codigo)+' - '+str(self.titulo)	

class Post(models.Model):
	forum = models.ForeignKey(Forum,blank=True,null=True)
	autor = models.ForeignKey(Usuario,blank=True,null=True)
	texto = models.CharField(max_length=3000,blank=True,null=True)
	data_post = models.DateTimeField(auto_now=False,null=False)
	pai = models.OneToOneField('self',null=True,blank=True)

	def __str__(self):
		return str(self.forum)+' - '+str(self.texto)

class Solicitacao(models.Model):
	tipo = models.CharField(max_length=20, null=True,blank=True)
	tipo_id = models.PositiveIntegerField()
	usuario = models.ForeignKey(Usuario)
	data_solicitacao = models.DateTimeField(auto_now=False,null=False)
	ativa = models.NullBooleanField()

	def __str__(self):
		if(self.tipo=='instituicao'):
			nome = Instituicao.objects.get(pk=self.tipo_id)
		elif(self.tipo=='curso'):
			nome = Curso.objects.get(pk=tipo_id)
		elif(self.tipo=='disciplina'):
			nome = Disciplina.objects.get(pk=tipo_id)
		elif(self.tipo=='turma'):
			nome = Turma.objects.get(pk=tipo_id)
		elif(self.tipo=='forum'):
			nome = Forum.objects.get(pk=tipo_id)
		return "Solicitação de inscrição - "+str(nome)