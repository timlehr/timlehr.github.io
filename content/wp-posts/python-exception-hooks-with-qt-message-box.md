Title: Python exception hooks with Qt message box
Date: 2018-01-29 00:45
Author: Tim Lehr
Category: Python, Qt
Slug: python-exception-hooks-with-qt-message-box
original_url: python-exception-hooks-with-qt-message-box/index.html
Status: published

When you develop complex applications or toolsets with Python, a good logging module and proper exception handling can save you a lot of headaches. Especially when those tools go into deployment, they are *never* bug-free and sooner or later people will tell you about all the unexpected issues they have. With proper logging you can pinpoint those bugs quickly, but often they happen in the most unlikely of places and you end up with an uncaught exception.

Depending on your application, uncaught exceptions might be completely invisible to the user, especially in applications developed with PySide / PyQt. If the user isn't looking at the stdout of your application or checking the logs, Pythons forgiving nature might make the user completely unaware that something bad happened, until it's too late. To deal with this issue, I recently adopted exception hooks in my Python applications, which allows me to hook custom functionality to the interpreter, in case an unhandled exception is raised during runtime. My solution is heavily inspired by the [QCrash report framework](https://github.com/ColinDuquesnoy/QCrash) developed by Colin Duquesnoy, minus the flexibility it provides. With just a couple of lines, it is however, much lighter.

``` line-numbers
import sys
import traceback
import logging
from Qt import QtCore, QtWidgets

# basic logger functionality
log = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
log.addHandler(handler)

def show_exception_box(log_msg):
    """Checks if a QApplication instance is available and shows a messagebox with the exception message. 
    If unavailable (non-console application), log an additional notice.
    """
    if QtWidgets.QApplication.instance() is not None:
            errorbox = QtWidgets.QMessageBox()
            errorbox.setText("Oops. An unexpected error occured:\n{0}".format(log_msg))
            errorbox.exec_()
    else:
        log.debug("No QApplication instance available.")
 
class UncaughtHook(QtCore.QObject):
    _exception_caught = QtCore.Signal(object)
 
    def __init__(self, *args, **kwargs):
        super(UncaughtHook, self).__init__(*args, **kwargs)

        # this registers the exception_hook() function as hook with the Python interpreter
        sys.excepthook = self.exception_hook

        # connect signal to execute the message box function always on main thread
        self._exception_caught.connect(show_exception_box)
 
    def exception_hook(self, exc_type, exc_value, exc_traceback):
        """Function handling uncaught exceptions.
        It is triggered each time an uncaught exception occurs. 
        """
        if issubclass(exc_type, KeyboardInterrupt):
            # ignore keyboard interrupt to support console applications
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
        else:
            exc_info = (exc_type, exc_value, exc_traceback)
            log_msg = '\n'.join([''.join(traceback.format_tb(exc_traceback)),
                                 '{0}: {1}'.format(exc_type.__name__, exc_value)])
            log.critical("Uncaught exception:\n {0}".format(log_msg), exc_info=exc_info)

            # trigger message box show
            self._exception_caught.emit(log_msg)
 
# create a global instance of our class to register the hook
qt_exception_hook = UncaughtHook()
```

Just paste it somewhere in one of your modules imported during application launch (preferably your logger) and you should be good to go. The code creates a new global object that hooks a function to the interpreter and also makes sure that said function is always executed on the main thread. This is important, since exceptions can occur on any thread - something that doesn't play nice with Qt widgets. If you have any issues with the code snippet, feel free to leave a comment. Happy coding, everyone!
