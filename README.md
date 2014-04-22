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


## Import Musical Data on the Server


Go to the directory where the MusicXML files are and sync the files with the server:

	cd Copy/Flauta\ Solo/Partituras/
	make sync
	
Go to the FlautaSolo directory and run the remote code to import the data:

	cd ~/Code/FlautaSolo
	make remote-import-data

## Import Musical Data Locally

To import data we need to create a virtualenvironment with Python 2.7, since Music21 doesn't work with Python 3:

	mkvirtualenv flauta-solo-django2

Install the requirements:

	pip install -r requirements

And install Music21:

    git clone https://github.com/cuthbertLab/music21.git
    cd music21
    python setup.py install

Run the command to import the files, for instance:

    ./manage.py importmusic /Users/kroger/Copy/Flauta\ Solo/Partituras/*.xml

## Deployment

To deploy:

	make deploy

## Server Setup

To install the dependencies on Webfaction (we don't use virtualenv on Webfaction):

    pip3.3 install --user -r requirements.txt
