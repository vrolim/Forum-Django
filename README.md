# SmartForum

Para configurar seu ambiente Python+Django, siga o seguinte tutorial:
- (http://pythonclub.com.br/instalacao-python-django-windows.html)
- Porém, ao invés de usar as versões indicadas no tutorial, instale:
- Python 3.5, Django 1.9


Faça o clone do repositório.

Um banco com a estrutura básica foi disponibilizado. Não necessitando assim realizar a migração do banco.

Usando o cmd, entre na pasta do projeto e digite os seguintes comandos:
- '''python manage.py runserver 8000''' //ou a porta que desejar. "Levanta/roda" a aplicação.

Foram criados dois usuários de teste:
- Admin do sistema: username=admin, password=admin123
- Usuário da aplicação com perfil de administrador da instituição: username=teste, password=admin123

Acesse no browser localhost:8000 //ou a porta que você indicou no runserver.

Para acessar o ambiente de administração da aplicação, o link é localhost:8000/admin. Digite o username e password do usuario admin do sistema.
