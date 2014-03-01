# minimum possible demo

install rabbitmq
> sudo apt-get install rabbitmq-server

Set up virtualenv, pip. Install requirements.
> pip install -r requirements.txt

install ta-lib

Download [ta-lib-0.4.0-src.tar.gz](http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz)
```
$ wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
$ tar -zxvf ta-lib-0.4.0-src.tar.gz
$ cd ta-lib
$ ./configure --prefix=/usr
$ make
$ sudo make install
```

install ta-lib wrapper
> pip install ta-lib

