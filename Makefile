# setting the PATH seems only to work in GNUmake not in BSDmake
PATH := ./pythonenv/bin:$(PATH)

runserver: dependencies
	./pythonenv/bin/python manage.py syncdb
	./pythonenv/bin/python manage.py runserver

generic_templates:
	sh -c 'echo p | svn co https://cybernetics.hudora.biz/intern/svn/code/projects/html/trunk/templates generic_templates'

dependencies: generic_templates
	virtualenv pythonenv
	pip -q install -E pythonenv -r requirements.txt

clean:
	rm -Rf pythonenv generic_templates build dist html test.db sloccount.sc .pylint.out
	rm -Rf pip-log.txt *.score
	rm -Rf pip-log.txt  coverage figleaf-exclude.txt .figleaf* .ropeproject
	find . -name '*.pyc' -or -name '*.pyo' -or -name 'svn-commit*tmp' | xargs rm
