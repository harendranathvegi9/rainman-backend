Rainman
=======

Rainman is a Chrome extension to provide background information on important terms in news articles online.

[http://rainman.io](http://rainman.io)

This application was originally developed in 24 hours by [Seth Thompson](http://seth.fm) & [Geoffrey Litt](http://geoffreylitt.com).
Rainman won first place at [Y-Hack 2013](http://y-hack.com/).

Backend
-------

The backend API is powered by a Flask app running NLTK, the Python Natural Language Processing (NLP) toolkit.

Quickstart
----------

###Prerequisites

* gcc
* Python 2.7
* [pip](https://pypi.python.org/pypi/pip) (package manager)
* [Virtualenv](https://pypi.python.org/pypi/virtualenv)
* [Alchemy API](http://www.alchemyapi.com/) key

###Installation

First, create a new Python Virtualenv in the root of the directory.

    $ virtualenv venv --distribute

Activate the virtualenv.  You must source the environment for each terminal session.

    $ source venv/bin/activate

Next, install the dependencies.

    $ pip install -r requirements.txt

Source the necessary API keys into environment variables:

    $ source keys

Finally, start the webapp using [Foreman](http://ddollar.github.io/foreman/).

    $ foreman start

Navigate to [http://localhost:5000](http://localhost:5000)!

Testing
-------

Rainman uses the [Nose](http://nose.readthedocs.org/) unittesting framework.

    $ nosetests

Profiling
---------

    $ python profile.py
