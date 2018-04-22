
GRANT ALL PRIVILEGES ON DATABASE julodoc TO julodoc_user;

pandoc -s -f markdown+tex_math_double_backslash example.md -t json -o example.json --mathjax

pypandoc.convert_file('example.md', 'html', format='markdown+tex_math_double_backslash', extra_args=['--mathjax'])

# i18n

* django-admin makemessages -l es
* django-admin compilemessages

# django

* python manage.py runserver
* python manage.py shell
* python manage.py makemigrations
* python manage.py migrate

# heroku

* heroku pg:reset # TODO check
* git push heroku master

