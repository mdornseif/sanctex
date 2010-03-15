Dies ist die Software fuer http://sanktionen.hudoracybernetics.com/

Siehe auch https://hudora.lighthouseapp.com/projects/42971/


# Developer box / Silvercloud installieren

Das ganze Setup ist dafür ausgelegt, mit [Silver Lining][1] zu funktionieren.
Silver Lining installiert man so:

    $ virtualenv -p python2.6 silver
    $ silver/bin/pip install -r http://bitbucket.org/ianb/silverlining/raw/tip/requirements.txt
    $ alias silver="/path/to/silver/bin/silver"

[1]: http://cloudsilverlining.org

Nun https://github.com/hudora/sanctex/raw/master/silver-build-layout.sh
herunterladen und ausführen.

    $ mkdir -P ~/code/with_silver_lining
    $ cd ~/code/with_silver_lining
    # Download https://github.com/hudora/sanctex/raw/master/silver-build-layout.sh
    $ sh silver-build-layout.sh sanctex-app
    $ cd sanctex-app/src/sanctex-src/sanctex
    $ make dependencies setup
    # losprogrammieren

Damit wirt ein virtualenv mit allem Zipp und Zapp aufgesetzt.

# Development

Wenn Silver Lining installiert ist, sollte man mit 

    make setup
    make runserver

einen Developmentserver starten können.


# Deployment

## Host einrichten

Zunächst muss man (zur Zeit bei Rackspace) einen Host starten und
konfigurieren. Wenn amn den Rackspace Accoutn konfiguriert hat, kann man
folgendermassen einen Server mit dem Namen `mischosting` an den Start bringen.

    $ silver create-node --image-id 14362 --size-id 1 mischosting
    $ silver setup-node mischosting
    $ ping -c 2 mischosting
    $ silver default-node mischosting

Das muss man natürlich nur einmal machen.

## Code deployen

Das geht dann einfach.

    $ make SILVERNODE=mischosting firstdeploy
    $ open http://mischosting/


# Further reading

* http://blog.maetico.com/post/383719182/toppcloud-the-5-minutes-tutorial
* http://blog.ianbicking.org/2010/01/29/new-way-to-deploy-web-apps/
* http://be.groovie.org/post/321827504/deploying-python-web-apps-with-toppcloud
* http://cloudsilverlining.org/django-quickstart.html
