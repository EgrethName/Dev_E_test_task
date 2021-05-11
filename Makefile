init-app:
	cd app && python3 manage.py makemigrations && python3 manage.py migrate

run:
	cd app && python3 manage.py runserver

test:
	cd app && python3 manage.py test -v 2 && cd ..

lint:
	pylint --load-plugins pylint_django --django-settings-module=dev_crud_task.settings app