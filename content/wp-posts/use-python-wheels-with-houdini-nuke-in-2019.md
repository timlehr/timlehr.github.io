Title: Use Python Wheels with Houdini / Nuke in 2019
Date: 2019-04-13 11:40
Author: Tim Lehr
Category: Houdini, Nuke, Python
Tags: Houdini
Slug: use-python-wheels-with-houdini-nuke-in-2019
original_url: use-python-wheels-with-houdini-nuke-in-2019/index.html
Status: published

During development of our pipeline toolset Scarif, I came across an issue with DCC Applications and certain Python packages. Since we are using quite a few open source Python modules to power our pipeline tools, we resort to a [virtual environment](https://virtualenv.pypa.io/en/latest/) in combination with [pip](https://pypi.org/project/pip/) to install and manage all these packages. Today, the almost all popular packages are usually distributed as a [Python Wheel](https://pythonwheels.com). Wheels are a modern approach to Python packaging and meant as the replacement for the ageing [Python Egg](https://setuptools.readthedocs.io/en/latest/formats.html) packaging solution. I wont go into details on the difference between the two solutions in this article, but if you are interested, feel free to have a look at [the official differentiation](https://packaging.python.org/discussions/wheel-vs-egg/). Extending a Python environment with a new *site-packages* directory containing packages such as eggs and wheels is a very easy thing to do.

### Pythonpath

``` line-numbers
export PYTHONPATH=$PYTHONPATH:/path/to/my/site-packages/
```

### At runtime

``` line-numbers
# register new site-packages directory with interpreter
import site
site.addsitedir("/path/to/my/site-packages/")
```

This is usually enough for the interpreter to be able to find and import modules. But even though Wheels are not that new anymore (introduced in 2012), some software packages like Houdini and Nuke still don't know how to deal with them. While the path is available to the interpreter, both Nuke and Houdini use an ancient version of setuptools (v0.6rc11, released in 2009), which is oblivious to the *.dist-info* directories created by wheels. setuptools is the crucial package when it comes to Python package management and didn't add support for .*dist-info *directories until v0.6.28. As the time of this writing setuptools has passed v41.0.0 and the reason behind Nuke and Houdini using such an outdated version of this package is still baffling to me.

## Teaching Nuke / Houdini some new tricks

Fortunately enough, the solution to this problem is fairly easy - and a little bit hacky. As we already know, the problem is setuptools, so replacing it with a more recent version should enable Nuke / Houdini to recognise and use any wheels in their environment. The be as unobtrusive as possible, I opted to import setuptools a new version at runtime from a location of my choice. As setuptools is installed with every virtual environment, all we need to do is add the site-package directory to our environment (see above) and re-import setuptools from there.

``` line-numbers
"""Put this code in your Python startup script file.
Nuke: init.py
Houdini: pythonrc.py 
"""

import importlib
import contextlib

def reimport_modules(*module_names):
    """Reimport modules by module name.
    """
    mod_iter = dict(sys.modules)
    for mod_name in module_names:
        for key, mod in mod_iter.iteritems():
            if hasattr(mod, "__file__") and mod_name in mod.__file__:
                sys.modules.pop(key)
                sys.modules[key] = importlib.import_module(key)
                print "Replaced imported module: '{}' // '{}' -> '{}'".format(mod.__name__,
                                                                              mod.__file__,
                                                                              sys.modules[key].__file__)

@contextlib.contextmanager
def prepend_site_packages(site_path):
    """Temporarily prepend ``site_path`` to sys.path.
    """
    orig_path = list(sys.path)
    try:
        sys.path.insert(0, str(site_path))
        yield
    finally:
        sys.path = orig_path

# temorarily modify environment and reload setuptools from newly added path
with prepend_site_packages("/path/to/site-packages"):
    reimport_modules("setuptools")
```

If you have any trouble getting this solution to work for you, [feel free shoot me a mail](mailto:03.must_gimlets@icloud.com) or get in touch on [twitter](https://twitter.com/punsolo). Happy coding!
