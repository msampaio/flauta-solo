SERVER = genosmus.com
APPNAME = flute

run-server:
	./manage-local.py runserver
	
tests:
	py.test

clean:
	find . -name *.pyc -exec rm {} \;

push:
	git push

deploy: push
	ssh $(SERVER) "cd ~/webapps/$(APPNAME)/$(APPNAME) && git pull && make restart-server"

remote-update-static-files:
	ssh $(SERVER) "cd ~/webapps/$(APPNAME)/$(APPNAME) && ./manage.py collectstatic -v0 --noinput"
	
remote-restart-server:
	ssh $(SERVER) "~/webapps/$(APPNAME)/apache2/bin/restart"

remote-see-errors:
	ssh $(SERVER) "cd ~/webapps/$(APPNAME)/$(APPNAME) && make see-errors"


## Database

initialize-development-database:
	psql -f data/initialize-database.sql
	./manage-local.py syncdb --noinput
	./manage-local.py migrate
	./manage-local.py loaddata data/adminuser.json
	
initialize-development-database-linux:
	echo "use genos_flute for the password"
	sudo -u postgres createuser -D -A -P genos_flute
	sudo -u postgres createdb -O genos_flute genos_flute
	./manage-local.py syncdb --noinput
	./manage-local.py migrate
	./manage-local.py loaddata data/adminuser.json
	
reset-development-database:
	psql -f data/reset-database.sql


## We should call these targets on the server only

see-errors:
	tail ~/logs/user/error_$(APPNAME).log
	echo "-----------------------------------------"
	tail ~/logs/frontend/error_$(APPNAME).log

restart-server:
	../apache2/bin/restart
