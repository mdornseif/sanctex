GAE_VERSION=1.6.5
APPID?= sanktex-hrd
REPOSNAME?=sanctex

GOOD_NAMES=
# pyLint
#   W0142 = *args and **kwargs support
# Pointless whinging
#   W0603 = Using the global statement
#   R0201 = Method could be a function
#   W0212 = Accessing protected attribute of client class
#   W0232 = Class has no __init__ method
#   W0212 = Access to a protected member _rev of a client class
# Mistakes in Parsing the AppEngine Source
#   E1103: %s %r has no %r member (but some types could not be inferred)
# Usually makes sense for webapp.Handlers & Friends.
#   W0221 Arguments number differs from %s method
# In Python versions < 2.6 all Exceptions inherited from Exception. py2.6 introduced BaseException
# On AppEngine we do not care much about the "serious" Exception like KeyboardInterrupt etc.
#   W0703 Catch "Exception"
#   R0903 Too few public methods - pointless for db.Models
# Unused Reports
#   RP0401 External dependencies
#   RP0402 Modules dependencies graph
#   RP0101 Statistics by type
#   RP0701 Raw metrics


PYLINT_ARGS= --output-format=parseable -rn -iy --ignore=config.py \
             --deprecated-modules=regsub,string,TERMIOS,Bastion,rexec,husoftm \
             --max-public-methods=25 \
             --max-line-length=110 \
             --min-similarity-lines=6 \
             --disable=I0011,W0201,W0142,W0603,W0403,R0201,W0212,W0232,W0212,E1103,W0221,W0703,W0404 \
             --disable=RP0401,RP0402,RP0101,RP0701,RP0801 \
             --ignored-classes=Struct,Model,google.appengine.api.memcache \
             --dummy-variables-rgx="_|dummy|abs_url" \
             --good-names=_,setUp,fd,application,$(GOOD_NAMES) \
             --generated-members=request,response

PYLINT_FILES= *.py ablage/

check: lib/google_appengine/google/__init__.py checknodeps fixup

checknodeps:
	@# pyflakes & pep8
	pep8 -r --ignore=E501 $(PYLINT_FILES)
	pyflakes $(PYLINT_FILES)
	@# der erste Durchlauf zeigt alle Probleme inkl. TODOs an
	-sh -c 'PYTHONPATH=`python config.py`:lib/google_appengine/ pylint $(PYLINT_ARGS) $(PYLINT_FILES)'
	# clonedigger *.py modules/ lib/CentralServices/ lib/gaetk/ lib/huTools lib/huSoftM

fixup:
	# Tailing Whitespace
	find modules -name '*.py' -print0 | xargs -0 perl -pe 's/[\t ]+$$//g' -i
	perl -pe 's/[\t ]+$$//g' -i templates/*.html
	# Tabs in Templates
	perl -MText::Tabs -ne 'print expand $$_' -i templates/*.html

# Install AppEngine SDK locally so pyLint und pyFlakes find it

lib/google_appengine/google/__init__.py:
	curl -s -O http://googleappengine.googlecode.com/files/google_appengine_$(GAE_VERSION).zip
	unzip -q google_appengine_$(GAE_VERSION).zip
	rm -Rf lib/google_appengine
	mv google_appengine lib/
	rm google_appengine_$(GAE_VERSION).zip

deploy:
	echo open http://dev-`whoami`.$(APPID).appspot.com/
	appcfg.py update -V dev-`whoami` -A $(APPID) .
	echo open http://dev-`whoami`.$(APPID).appspot.com/
	TESTHOST=dev-`whoami`.$(APPID).appspot.com make resttest
	echo open http://dev-`whoami`.$(APPID).appspot.com/
	open http://dev-`whoami`.$(APPID).appspot.com/
	
deploy_production:
	# wir legen ein komplett neues tmp verzeichnis mit einem sauberen checkout an und gehen von da weiter
	rm -Rf tmp
	mkdir tmp
	(cd tmp ; git clone git@github.com:hudora/$(REPOSNAME).git)
	(cd tmp/$(REPOSNAME) ; git checkout production ; make dependencies)
	(cd tmp/$(REPOSNAME) ; git show-ref --hash=7 refs/remotes/origin/production > version.txt)
	# Erst getaggte Version hochladen
	appcfg.py update -V "v`cat tmp/$(REPOSNAME)/version.txt`" -A $(APPID) tmp/$(REPOSNAME)
	# Dann testen
	(cd tmp/$(REPOSNAME) ; TESTHOST="v`cat version.txt`".$(APPID).appspot.com make resttest)
	# Wenn das geklappt hat: produktionsversion aktivieren.
	appcfg.py update -V production -A $(APPID) tmp/$(REPOSNAME)
	appcfg.py backends -V production -A $(APPID) tmp/$(REPOSNAME) update
	curl -s -u d51d515b8db83d0d7da6fe88572b5c6eb7510b9e:X -H 'Content-Type: application/json' -d "{'message':{'body':'$(REPOSNAME) production `cat tmp/$(REPOSNAME)/version.txt` nach http://sanktex-hrd.appspot.com deployed von `id -un` auf `hostname`'}}" https://hudora.campfirenow.com/room/342697/speak.json > /dev/null
	open http://sanktex-hrd.appspot.com/spezial/changelog.html

openlogs:
	open "https://appengine.google.com/logs?app_id=s%7E$(APPID)&version_id=dev-`whoami`"

opendev:
	open http://dev-`whoami`.$(APPID).appspot.com/
	echo open http://dev-`whoami`.$(APPID).appspot.com/

next_production:
	# differences to next production deploy
	git fetch origin
	git log --color --pretty=oneline --abbrev-commit 'origin/production..' | sed 's/^/  /'

clean:
	find . -name '*.pyc' -or -name '*.pyo' -delete
	git submodule foreach "make clean||:"

dependencies: clean
	git submodule update --init

resttest: dependencies
	sh -c "PYTHONPATH=.:lib/huTools python tests/resttest.py --hostname=$(TESTHOST) --credentials-user=$(CREDENTIALS_USER)"

    .PHONY: deploy pylint dependencies_for_check_target clean check dependencies

