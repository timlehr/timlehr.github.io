Title: Nuke: Environment Variables in Read / Write
Date: 2019-04-11 09:18
Author: Tim Lehr
Category: Nuke, Python
Tags: Environment, Nuke, Python
Slug: nuke-environment-variables-in-read-write
original_url: nuke-environment-variables-in-read-write/index.html
Status: published

In my job as a Pipeline TD I often resort to old school [environment variables](https://en.wikipedia.org/wiki/Environment_variable) to make my life easier. Not only are they really easy to work with, they are also a commonly supported way of keeping file paths relative to a dynamically changeable directory. This is super helpful, as you will be able to open your existing production files in a different location, without the need to change any of the paths hardcoded into it. If you are a Maya or Houdini user, you are probably very familiar with paths like this: *\$SHOT_ROOT/scene_v001.ma*

Wouldn't it be cool to have the same solution in Nuke for Read / Write (or any other node for that matter)? Unfortunately, out of the box, a path like this will not work in Nuke at all and throw an error to the user. So to make this work we need to take care of resolving the variable ourselves. So far I've found multiple solutions for this - if you know of a better one, please [shoot me a mail](mailto:03.must_gimlets@icloud.com).

## Filename Filter Callback

The most powerful and simplest approach to take control over Nukes filepath evaluation is a [filenameFilter callback](https://learn.foundry.com/nuke/developers/6.3/pythondevguide/callbacks.html#filenamefilter).

``` line-numbers
def filter_envvars_in_filepath(filename):
    """Expand variables in path such as ``$PROJECT_ROOT``.
    """
    expanded_path = os.path.expandvars(filename)
    return expanded_path

# register callback
nuke.addFilenameFilter(filter_envvars_in_filepath)
```

You can register this Python callback anywhere you like, though I would recommend doing so in a [*init.py* (or *menu.py*) file](https://learn.foundry.com/nuke/developers/112/pythondevguide/startup.html). The snippet will take care of replacing any variables in paths processed by Nuke with the corresponding values stored in the Python environment (*os.environ*). If a variable is not set, no changes will be made to it.

### What about Terminal Mode / Frame Server?

The previously stated solution requires the filename filter to be registered every time you want to use your Nuke scripts with environment variables in your nodes. However, in some cases, this can prove difficult to set up. Depending on your render farm environment, it's not always the most reliable solution. This also applies if are using the Nuke 11 Frame Server to speed up your renderings using multi-processing on a single machine. In these cases, the Nuke script is only every *read* *in background*, so we can apply a somewhat dirty hack to resolve the environment variable in it's place.

``` line-numbers
def add_oncreate_code():
    """ Expand environment variables on node creation in non-gui mode
    """
    node = nuke.thisNode()
    node.knob("onCreate").setValue("""
    import nuke
    if "-t" in nuke.rawArgs: # non-gui check
        node = nuke.thisNode()
        knob = node.knob("file")
        filename = knob.value()
        expanded_path = os.path.expandvars(filename)
        knob.setValue(expanded_path)
    """)
    
nuke.addOnCreate(add_oncreate_code, nodeClass='Read')
nuke.addOnCreate(add_oncreate_code, nodeClass='Write')
```

This code snippet is adding a small piece of Python code to every Read / Write node, which will replace any variables in it's "file" knob *permanently*. Since this is quite destructive, we only ever want to use this when we are sure our render is running in the background and the Nuke script is *not* being saved after the render completed, e.g. render farm or frame server. Like the previous snippet you should call this code in your *init.py* or *menu.py* file.

**Side note:** As I learned recently, detecting if Nuke is running in terminal mode can be quite deceptive. While there is a variable called *nuke.INTERACTIVE*, it's unfortunately just an indicator if Nuke is using an interactive license. For a more reliable solution I would recommend checking the command line arguments of the process and look out for [any terminal arguments](https://learn.foundry.com/nuke/content/comp_environment/configuring_nuke/command_line_operations.html#UsingcommandlineFlags).

``` python
in_terminal_mode = "-t" in nuke.rawArgs
```

## Update TCL Environment from Python

Another solution would be updating the TCL environment with the necessary environment variables from Python. While the Nuke Python interpreter picks up the environment it's running in, for any TCL code, we first need to set them manually. This includes the "file" knob of Read / Write nodes, which uses the TCL to look up it's variables. This method is definitely inferior and a lot of pitfalls, since you need to manually keep the TCL environment in sync with Python and once again run into trouble once you render in background. For those of you interested, here is a simple solution on how you would get TCL to match your *os.environ *in Python.

``` line-numbers
# iterate over environment and set it in TCL
for key, value in os.environ.iteritems():
    nuke.tcl("set", key, value)
```