# setting the PATH seems only to work in GNUmake not in BSDmake
PATH := ../../bin:$(PATH)
SILVERNODE := sanctex.local

runserver: dependencies
	silver serve ../..

deploy: dependencies
	silver update --node $(SILVERNODE) ../..
	(cd ../../; silver run $(SILVERNODE) manage.py syncdb)

#generic_templates:
#	sh -c 'echo p | svn co https://cybernetics.hudora.biz/intern/svn/code/projects/html/trunk/templates generic_templates'

setup: dependencies
	../../bin/manage.py syncdb --noinput

dependencies:
	../../bin/pip -q install -r ./requirements.txt

clean:
	find . -name '*.pyc' -or -name '*.pyo' | xargs rm
