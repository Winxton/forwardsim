# prehack setup

install rabbitmq
```sudo apt-get install rabbitmq-server```

Set up virtualenv, pip. Install requirements.
```pip install -r requirements.txt```

install ta-lib ([ta-lib-0.4.0-src.tar.gz](http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz))
```
$ wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
$ tar -zxvf ta-lib-0.4.0-src.tar.gz
$ cd ta-lib
$ ./configure --prefix=/usr
$ make
$ sudo make install
```

install ta-lib wrapper

```pip install ta-lib```
or
```easy_install ta-lib```

initialize submodules
```
git submodule init
git submodule update
```

## Development

start web server
```python server.py```

start celery
```./startcelery``` or ```celery -A flaskcelery.tasks.celery worker --loglevel=INFO```
