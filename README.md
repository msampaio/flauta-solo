## Instalation and Requirements

It's useful to add the following configuration in your ~/.ssh/config:

	Host genosmus.com
  		User genos

Create a virtualenv that uses Python 3:

	brew install python3
	mkvirtualenv -p /usr/local/bin/python3 flauta-solo-django

Install the requirements:

	pip install -r requirements.txt


## Deployment

To deploy:

	make deploy
