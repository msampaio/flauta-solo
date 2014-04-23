SERVER = genosmus.com
APPNAME = flute
TODAY = $(shell date '+%Y-%m-%d')
DATABASE = genos_flute

runserver:
	./manage.py runserver
	
tests:
	py.test

clean:
	find . -name *.pyc -exec rm {} \;

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

import-server-data2:
	ssh $(SERVER) "pg_dump $(DATABASE) -U genos_flute -F t -w | gzip > database/flute-$(TODAY).dump.gz"
	scp $(SERVER):database/flute-$(TODAY).dump.gz /tmp/
	psql -f data/reset-database.sql
	psql -f data/initialize-database.sql
	gunzip -c /tmp/flute-$(TODAY).dump.gz | pg_restore -C -d $(DATABASE)

initialize-dev-database-with-data-from-server:
	$(MAKE) reset-development-database
	$(MAKE) initialize-development-database
	$(MAKE) import-server-data

import-server-data:
	ssh $(SERVER) "cd ~/webapps/$(APPNAME)/$(APPNAME) && ./manage-production.py dumpdata | gzip -c > ~/database/flute-$(TODAY).data.gz"
	scp $(SERVER):database/flute-$(TODAY).data.gz /tmp/
	./manage.py loaddata /tmp/flute-$(TODAY).data.gz

initialize-development-database:
	psql -f data/initialize-database.sql
	./manage.py syncdb --noinput
	./manage.py migrate
	#./manage.py loaddata data/adminuser.json
	
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
