APPID?= sanktex-hrd
REPOSNAME?=sanctex


MYPYTHONPATH=lib/site-packages

-include ./lib/appengine-toolkit/include.mk

# TODO: wie werden die Module API und sync geupdated
# appcfg.py update -A e~hudoraexpress sync.yaml
# appcfg.py update -A e~hudoraexpress api.yaml

boot:
	# https://cloud.google.com/sdk/docs/quickstart-mac-os-x ; gcloud init
	# oder gcloud components update
	git submodule update --init
	pip install --upgrade --target lib/site-packages -r requirements.txt

code:
	echo "nothing to do"