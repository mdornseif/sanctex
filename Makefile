deploy: check
	appcfg.py update .

check: lib/google_appengine/google/__init__.py
	pep8 -r --ignore=E501 sanctions/ *.py
	sh -c 'PYTHONPATH=`python config.py` pyflakes *.py sanctions/'
	-sh -c 'PYTHONPATH=`python config.py` pylint -iy --max-line-length=110 *.py sanctions/' # -rn

# Appengine SDK lokal installieren, damit pyLint und pyFlakes das finden
lib/google_appengine/google/__init__.py:
	curl -O http://googleappengine.googlecode.com/files/google_appengine_1.3.8.zip
	unzip google_appengine_1.3.8.zip
	rm -Rf lib/google_appengine
	mv google_appengine lib/
	rm google_appengine_1.3.8.zip

dependencies: clean
	git submodule update --init 
	curl -O http://ec.europa.eu/external_relations/cfsp/sanctions/list/version4/global/global.xml

clean:
	find . -name '*.pyc' -or -name '*.pyo' -delete

.PHONY: deploy pylint dependencies_for_check_target clean check dependencies
