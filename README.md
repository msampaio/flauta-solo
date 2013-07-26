FlautaSolo
==========

Estudo do repertório de flauta solo.

# Links

* [GenosLab](http://genosmus.com/pesquisa/flauta-solo/)
* [IMSLP](http://imslp.org/)

# Instalação

Para usar o FlautaSolo é preciso ter o [Python](http://python.org/),
[VirtualEnv](http://genosmus.com/handbook/python/),
[Git](http://git-scm.com/) e [Music21](http://mit.edu/music21/)
instalados. O Python vem instalado por padrão em Macintosh e Linux.

## Criação de um ambiente no Virtualenv

Para criar o ambiente `flautaSolo`, abra um terminal e rode:

    $ mkvirtualenv flautaSolo

## Instalação do FlautaSolo

No terminal ative o ambiente `flautaSolo`:

    $ workon flautaSolo

Entre em um diretório onde queira colocar o programa FlautaSolo e
baixe com o Git:

    $ git clone https://github.com/GenosResearchGroup/FlautaSolo.git

Uma boa sugestão é salvar o arquivo em um diretório como `~/src` ou
`~/Code` (no Mac e Linux). No Windows pode ser algo como `C:\Code`.

Entre no diretório `FlautaSolo` que você baixou e rode os comandos:

    $ pip install ipython
    $ pip install numpy
    $ pip install matplotlib
    $ pip install -r requirements.txt

## Instalação do Music21

Baixe a cópia do Music21 mantida pelo Genos:

    $ git clone https://github.com/GenosResearchGroup/music21.git

Entre no diretório `music21` e baixe o branch `contour`:

    $ git branch --track contour origin/contour
    $ git checkout contour

Verifique se você está no branch `contour`

    $ git branch

Ainda no diretório `music21` ative o ambiente `flautaSolo` no
Virtualenv e rode:

    $ python setup.py install

# Uso do FlautaSolo

Ative o ambiente `flautaSolo` do Virtualenv, entre no diretório `FlautaSolo` e rode:

    $ ipython

Dentro do ambiente do `Ipython` importe o pacote `analysis`:

    >>> import analysis

Para trabalhar com o Music21, importe o pacote `music21`:

    >>> import music21
