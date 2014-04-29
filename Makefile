SERVER = genosmus.com
APPNAME = flute
TODAY = $(shell date '+%Y-%m-%d')
DATABASE = genos_flute
DATABASE_DUMP = flute-$(TODAY).json.gz

runserver:
	./manage.py runserver
	
tests:
	py.test

clean:
	find . -name *.pyc -exec rm {} \;
	-find . -name "__pycache__" -exec rm -rf {} \;

push:
	git push

deploy: push
	ssh $(SERVER) "cd ~/webapps/$(APPNAME)/$(APPNAME) && git pull && make restart-server"

remote-import-data:
	ssh $(SERVER) "cd ~/webapps/$(APPNAME)/$(APPNAME) && python2.7 manage-production.py importmusic ~/partituras-flauta/*.xml"

remote-update-static-files:
	ssh $(SERVER) "cd ~/webapps/$(APPNAME)/$(APPNAME) && ./manage-production.py collectstatic -v0 --noinput"
	
remote-restart-server:
	ssh $(SERVER) "~/webapps/$(APPNAME)/apache2/bin/restart"

remote-see-errors:
	ssh $(SERVER) "cd ~/webapps/$(APPNAME)/$(APPNAME) && make see-errors"

## Database

reset-dev-database-with-data-from-server:
	$(MAKE) reset-development-database
	$(MAKE) initialize-development-database
	$(MAKE) import-server-data

import-server-data:
	ssh $(SERVER) "cd ~/webapps/$(APPNAME)/$(APPNAME) && ./manage-production.py dumpdata analysis | gzip -c > ~/database/$(DATABASE_DUMP)"
	scp $(SERVER):database/$(DATABASE_DUMP) /tmp/
	./manage.py loaddata /tmp/$(DATABASE_DUMP)

initialize-development-database:
	psql -f data/initialize-database.sql
	./manage.py syncdb --noinput
	./manage.py migrate
	./manage.py loaddata data/adminuser.json
	
initialize-development-database-linux:
	echo "use genos_flute for the password"
	sudo -u postgres createuser -D -A -P genos_flute
	sudo -u postgres createdb -O genos_flute genos_flute
	./manage.py syncdb --noinput
	./manage.py migrate
	./manage.py loaddata data/adminuser.json
	
reset-development-database:
	psql -f data/reset-database.sql


## We should call these targets on the server only

import-data:
	python2.7 manage-production.py importmusic ~/partituras-flauta/*.xml

see-errors:
	tail ~/logs/user/error_$(APPNAME).log
	echo "-----------------------------------------"
	tail ~/logs/frontend/error_$(APPNAME).log

restart-server:
	../apache2/bin/restart
