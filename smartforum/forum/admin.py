from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from forum.models import *

class UsuarioInline(admin.StackedInline):
	model = Usuario
	can_delete = False
	verbose_name_plural = "Usuários"

class UserAdmin(BaseUserAdmin):
	inlines = (UsuarioInline,)

admin.site.unregister(User)
admin.site.register(User,UserAdmin)

class InstituicaoAdmin(admin.ModelAdmin):
    list_display = ('sigla','nome','cnpj','email',)
    filter_horizontal = ('usuarios',)
admin.site.register(Instituicao, InstituicaoAdmin)

class CursoAdmin(admin.ModelAdmin):
    list_display = ('codigo_mec','nome','instituicao',)
    filter_horizontal = ('usuarios',)
admin.site.register(Curso, CursoAdmin)

class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('codigo','nome',)
    filter_horizontal = ('usuarios','curso',)
admin.site.register(Disciplina, DisciplinaAdmin)

class TurmaAdmin(admin.ModelAdmin):
    list_display = ('codigo','nome',)
    filter_horizontal = ('alunos','professores','tutores',)
admin.site.register(Turma, TurmaAdmin)

class ArquivoAdmin(admin.ModelAdmin):
    list_display = ('nome','tipo','turma',)
admin.site.register(Arquivo, ArquivoAdmin)

class ForumAdmin(admin.ModelAdmin):
    list_display = ('turma','titulo','criador',)
admin.site.register(Forum, ForumAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('forum','autor',)
admin.site.register(Post, PostAdmin)

class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = ('tipo','usuario',)
admin.site.register(Solicitacao, SolicitacaoAdmin)