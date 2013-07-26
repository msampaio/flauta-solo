FlautaSolo
==========

Estudo do repertório de flauta solo.

# Links

* [GenosLab](http://genosmus.com/pesquisa/flauta-solo/)
* [IMSLP](http://imslp.org/)

# Instalação

Para usar o FlautaSolo é preciso ter o
[Python](http://python.org/),
[VirtualEnv](http://genosmus.com/handbook/python/) e
[Git](http://git-scm.com/) instalados. O Python vem instalado por
padrão em Macintosh e Linux.

Abra um terminal e baixe o programa FlautaSolo:

    $ git clone https://github.com/GenosResearchGroup/FlautaSolo.git

Crie um ambiente `flautaSolo`:

    $ mkvirtualenv flautaSolo

Ative o ambiente:

    $ workon flautaSolo

Entre no diretório `FlautaSolo` que você baixou e rode os comandos:

    $ pip install ipython
    $ pip install numpy
    $ pip install matplotlib
    $ pip install -r requirements.txt
