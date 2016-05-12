from django.conf.urls import url
from forum import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.index),
    url(r'^entrar/$', views.entrar),
    url(r'^cadastro/$', views.cadastro),
    url(r'^sair/$', views.sair),
    url(r'^home/$', views.home),
    url(r'^painel/$', views.painel),
    url(r'^add/(?P<tipo>[\w]+)/(?P<tipo_id>[\0-9]+)$', views.add),
    url(r'^visualizacao/(?P<tipo>[\w]+)/(?P<tipo_id>[\0-9]+)$', views.visualizacao),
    url(r'^listar/(?P<tipo>[\w]+)$', views.listar),
    url(r'^novo/(?P<tipo>[\w]+)$', views.novo),
    url(r'^interacao/(?P<forum_id>[\0-9]+)$', views.interacao),
    url(r'^solicitacao/(?P<solicitacao_id>[\0-9]+)/(?P<resposta>[\0-9]+)$', views.solicitacao),
]