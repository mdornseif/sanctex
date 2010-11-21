Dies ist die Software fuer http://sanktionen.hudoracybernetics.com/

Siehe auch https://hudora.lighthouseapp.com/projects/42971/


virtualenv tmpenv 
tmpenv/Scripts/activate 
pip install -r requirements.txt 

Then you have to manually copy each lib from tmpenv/lib to the project root. djangoappengine have to be installed manually, because it does not have setup.py ( http://bitbucket.org/wkornewald/djangoappengine/issue/17/setuppy-file (this link goes outside odesk.com) ). Then tmpenv can be deleted. Or you can manually install each dependency. It is ugly, but author of djangoappengine preferred this way (djangoappengine expects that it is placed at project root and will not work if it is not). I attached my project dir as it is (without .git folder).

To deploy it, you can run: 

manage.py deploy 

Then call http://domain.appspot.com/download/ (this link goes outside odesk.com) . This will start app engine queue to process global.xml . This page can answer with 500 Error, but AFAIK it's ok, log should look like: 

CancelledError: The API call taskqueue.BulkAdd() was explicitly cancelled. 

This happens because I catch DeadlineExceededError and add task to continue work from saved point.
