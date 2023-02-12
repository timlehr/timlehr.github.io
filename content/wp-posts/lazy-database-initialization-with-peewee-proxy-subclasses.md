Title: Lazy database initialization with peewee proxy subclasses
Date: 2018-01-31 22:36
Author: Tim Lehr
Category: Python, SQL
Slug: lazy-database-initialization-with-peewee-proxy-subclasses
original_url: lazy-database-initialization-with-peewee-proxy-subclasses.html
Status: published

If you are working with a SQL database in Python, I highly recommend to take a look at [peewee](https://peewee.readthedocs.io/en/latest/). It's a small, but very powerful ORM (Object relational mapping) tool that makes the interaction with your database very pythonic, convenient and quite easy to learn (especially for the SQL beginners among you). I personally use peewee for my production pipeline tool-set called *Scarif*, which I currently develop with a fellow TD here at Filmakademie. So far, peewee has been an invaluable package for us, that saves us a lot of time during development.

One of my favorite peewee features is it's ability to initialize the python database models during runtime by providing the database with a proxy backend. This allows you to choose your database backend at runtime (e.g. *MySQL*, *SQLite* or *PostgreSQL*) and supply database connection credentials for example via config-file. Usually your base-model class with a proxy in place looks somewhat like this:

``` line-numbers
from peewee import *

global_database_object = Proxy()

class BaseModel(Model):
    """Basemodel from which all other peewee models are derived.
    """

    class Meta:
        database = global_database_object
```

If you now want to initialize your database with a real backend of your choice during runtime, you'll have to call the initialization function on the proxy before using the database in any way or otherwise you will be greeted with an exception.

``` line-numbers
my_runtime_db = MySQLDatabase('myDatabaseName',
                                **{'host': 'localhost',
                                'user': 'root'
                                'password': "superS3cr3t",
                                'port': 3306,
                                })
global_database_object.initialize(my_runtime_db)
```

It's as easy as that. Sometimes however, you might have a lot of different applications and tools accessing the database, so you will always have to remember to do the initialization first thing. Wouldn't it be nice if you could just let peewee handle this call for you, so you don't have to worry about anything? To do this, you only need a subclass of the peewee proxy as well as a couple of lines of code.

``` line-numbers
class CustomProxy(Proxy):
    """Simple :obj:`peewee.proxy` subclass that tries to initialize the DB proxy on-demand.
    """
    def __getattr__(self, attr):
        """ If a member of the proxy is being accessed, 
            and it's not yet initialized (obj == None), try initialization.
        """
        if self.obj is None:
            self.initialize_proxy()
        return super(ScProxy, self).__getattr__(attr)

    def initialize_proxy():
        """Helper function that initializes the proxy with credentials read from somewhere else (e.g. config-file). 
        For demonstration purposes, they are hardcoded though. :) 
        """
        log.debug("Access to uninitialized DB proxy requested. Try initialization ...")
        lazy_loaded_db= MySQLDatabase('myDatabaseName',
                                **{'host': 'localhost',
                                'user': 'root',
                                'password': "superS3cr3t",
                                'port': 3306
                                })
        self.initialize(lazy_loaded_db)

global_database_object = CustomProxy()
```

This little subclass takes care of everything. Whenever something or someone is trying to use the proxy, the proxy will check if it's initialized and try to do so if it's not. This way you make the initialization on-demand. Now for some scenarios this might not be acceptable, since you are really initializing as late as possible and delaying the actual (first) request, but in most cases you'll be fine. Here is the full example code for your enjoyment. Happy coding.

``` line-numbers
from peewee import *
import logging 

log = logging.get_logger(__name__)

class CustomProxy(Proxy):
    """Simple :obj:`peewee.proxy` subclass that tries to initialize the DB proxy on-demand.
    """
    def __getattr__(self, attr):
        """ If a member of the proxy is being accessed, 
            and it's not yet initialized (obj == None), try initialization.
        """
        if self.obj is None:
            self.initialize_proxy()
        return super(ScProxy, self).__getattr__(attr)

    def initialize_proxy():
        """Helper function that initializes the proxy with credentials read from somewhere else (e.g. config-file). 
        For demonstration purposes, they are hardcoded though. :) 
        """
        log.debug("Access to uninitialized DB proxy requested. Try initialization ...")
        lazy_loaded_db= MySQLDatabase('myDatabaseName',
                                **{'host': 'localhost',
                                'user': 'root',
                                'password': "superS3cr3t",
                                'port': 3306
                                })
        self.initialize(lazy_loaded_db)

global_database_object = CustomProxy()

class BaseModel(Model):
    """Basemodel from which all other peewee models are derived.
    """

    class Meta:
        database = global_database_object
```
