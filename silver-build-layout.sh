#!/usr/bin/env bash

DIR="$1"
PROJECT="sanctex"

if [ -z "$DIR" ] ; then
    echo "$(basename $0) DIR"
    echo "execute his OUTSIDE a repository / checkout"
    exit 2
fi

if [ ! -e "$DIR/bin/python" ] ; then
    silver init "$DIR"
fi

cd "$DIR"
MAIN_REPRO="git@github.com:hudora/sanctex.git"
LIB_REPRO="git@github.com:ianb/zamboni-lib.git"
# for R/O access it is something like
#MAIN_REPRO="git://github.com/ianb/zamboni.git"
#LIB_REPRO="git://github.com/ianb/zamboni-lib.git"

if [ ! -e src/$PROJECT-src ] ; then
    mkdir src/$PROJECT-src
fi

if [ ! -e src/$PROJECT-src/$PROJECT/.git ] ; then
    #git clone --recursive $MAIN_REPRO src/zamboni-src/zamboni
    git clone $MAIN_REPRO src/$PROJECT-src/$PROJECT
    #pushd src/($PROJECT)-src/zamboni
    #git submodules update --init
    #popd
fi

if [ ! -L app.ini ] ; then
    rm app.ini
    ln -s src/$PROJECT-src/$PROJECT/silver-app.ini app.ini
fi

if [ ! -e lib/python/silvercustomize.py ] ; then
    echo "import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
" > lib/python/silvercustomize.py
fi

if [ ! -e lib/python/$PROJECT.pth ] ; then
    echo "../../src/$PROJECT-src/$PROJECT/" > lib/python/$PROJECT.pth
fi

#if [ ! -e lib/python/.git ] ; then
#    git clone $LIB_REPRO lib/python
#fi

if [ ! -L bin ] ; then
    if [ -z lib/python/bin/ ] ; then
        mv bin/* lib/python/bin/
        rmdir bin/
        ln -s lib/python/bin bin
    fi
fi

if [ ! -L bin/manage.py ] ; then
    if [ -e src/$PROJECT-src/$PROJECT/manage.py ] ; then
        ln -s src/$PROJECT-src/$PROJECT/manage.py bin/manage.py
    fi
fi

if [ ! -L static/media ] ; then
    cd static
    ln -s ../src/$PROJECT-src/media media
    cd ..
fi

./bin/pip install -r src/$PROJECT-src/$PROJECT/requirements.txt

# if [ ! -e src/django-debug-toolbar ] ; then
#     git clone git://github.com/robhudson/django-debug-toolbar.git src/django-debug-toolbar
# fi
# 
# if [ ! -e src/django-debug-cache-panel ] ; then
#     git clone git://github.com/jbalogh/django-debug-cache-panel src/django-debug-cache-panel
# fi
# 
# if [ ! -e src/django-extensions ] ; then
#     git clone git://github.com/django-extensions/django-extensions.git src/django-extensions
# fi
