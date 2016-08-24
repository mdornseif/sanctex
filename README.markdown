Dies ist die Software fuer http://sanktionen.cyberlogi.de/



Deployment
==========

Production
----------

Wenn alles zufriedenstellend ist, kann der **Produktions-Branch** geupdated werden. Da geht so:

    git clone git@github.com:hudora/sanctex.git
    cd sanctex/
    git checkout production
    git merge --no-ff origin/production  # falls man keinen clean checkout hat
    git log --pretty=oneline --abbrev-commit origin/production..origin/master > CHANGELOG.tmp
    git merge --no-ff origin/master
    cat CHANGELOG.markdown >> CHANGELOG.tmp
    mv CHANGELOG.tmp CHANGELOG.markdown
    subl CHANGELOG.markdown

Nun müssen End-User relevante Änderungen in der Datei CHANGELOG.markdown bechrieben werden.
Wenn alle Änderungen akzeptabel & Akzeptiert sind, kann gemerged werden.

    git commit -m 'CHANGELOG angepasst' CHANGELOG.markdown
    git push origin production
    git checkout master
    make deploy_production
    rm -Rf tmp
