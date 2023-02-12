Title: Export all Maya render layers as ASS files using Python
Date: 2019-04-06 23:22
Author: Tim Lehr
Category: Arnold, Maya
Tags: Arnold, Maya, Python
Slug: export-all-maya-render-layers-as-ass-files-using-python
original_url: export-all-maya-render-layers-as-ass-files-using-python.html
Status: published

You would think exporting all render layers in Maya to *Arnold Scene Source* (.ass) files could be done without much hassle. So did I. To be fair, any confusion over this matter is a result of Mayas new render setup introduced a few years ago. At the time of this writing, Arnold can only export geometry and settings from the currently active render layer. To conveniently switch render layers for export while maintaining the current scene state for the artist, we can write ourselves a small context manager.

``` line-numbers
import contextlib
import maya.app.renderSetup.model.renderSetup as renderSetup

@contextlib.contextmanager
def maintained_render_layer():
    previous_rs = renderSetup.instance().getVisibleRenderLayer()
    try:
        yield
    finally:
        renderSetup.instance().switchToLayer(previous_rs)
```

Now we can use another code snippet to conveniently export all render layers to ASS files.

``` line-numbers
import maya.app.renderSetup.model.renderSetup as renderSetup
import pymel.core as pm

export_options = {} # supply your own arnoldExportAss options here         
with maintained_render_layer():
    for layer in renderSetup.instance().getRenderLayers():
        layer_name, layer_obj = render_layer
        mayautil.set_current_render_layer(layer_obj)
        print("Run ASS Export for render layer "
              "'{}' with options: '{}'".format(layer.name(), export_options))
        pm.other.arnoldExportAss(**export_options)
```

Check out this thread for [available arnoldExportAss options](https://answers.arnoldrenderer.com/questions/3652/flags-for-mayacmdsarnoldexportass.html).
