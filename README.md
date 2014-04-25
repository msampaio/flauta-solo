## Install Postgres

On the Mac the easiest way is to install the Postgress package: http://postgresapp.com

Add the following to your ~/.bashrc:

	export PATH="/Applications/Postgres.app/Contents/Versions/9.3/bin:$PATH"

## Instalation and Requirements

It's useful to add the following configuration in your ~/.ssh/config:

	Host genosmus.com
  		User genos

Create a virtualenv that uses Python 3:

	brew install python3
	mkvirtualenv -p /usr/local/bin/python3 flauta-solo-django

Install the requirements:

	pip install -r requirements.txt

On the Mac you may need to use the following command:

	export ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future

## Initialize the Database

Initialize the database with:

	make initialize-development-database

## Import Data From The Server

You can copy the current data on the server's database and load on your development
environment by running the command:

    make reset-dev-database-with-data-from-server

Keep in mind that this will **delete all the data on the local development's database**

## Run the Local Development Server

You can run the local dev server with:

	make
	
Two another options are:

	make runserver
	
or

	./manage.py runserver

## Import Musical Data on the Server

Go to the directory where the MusicXML files are and sync the files with the server:

	cd Copy/Flauta\ Solo/Partituras/
	make sync
	
Go to the FlautaSolo directory and run the remote code to import the data:

	cd ~/Code/FlautaSolo
	make remote-import-data

## Deployment

To deploy:

	make deploy

## Server Setup

To install the dependencies on Webfaction (we don't use virtualenv on Webfaction):

    pip3.3 install --user -r requirements.txt
    pip2.7 install git+https://github.com/GenosResearchGroup/music21.git@contour

## Import Musical Data Locally

You don't need to follow these steps. It's better to load the data from the server database instead.
To import data we need to create a virtualenvironment with Python 2.7, since Music21 doesn't work with Python 3:

	mkvirtualenv flauta-solo-django2

Install the requirements:

	pip install -r requirements

And install Music21:

    pip install git+https://github.com/GenosResearchGroup/music21.git@contour

Run the command to import the files, for instance:

    ./manage.py importmusic /Users/kroger/Copy/Flauta\ Solo/Partituras/*.xml

