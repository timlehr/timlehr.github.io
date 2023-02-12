Title: Python Scripting in DaVinci Resolve
Date: 2018-12-30 19:36
Author: Tim Lehr
Category: Editorial, Python
Tags: DaVinci, Python
Slug: python-scripting-in-davinci-resolve
original_url: python-scripting-in-davinci-resolve.html
Status: published

Starting with *DaVinci Resolve 15*, Developer Blackmagic added new Scripting functionality to the popular Editing / Grading Suite. The Scripting API (Fusion Script) is implemented in a separate executable called *fuscript,* which supports two languages at the time of writing: Python 2.7 / 3 and Lua. The integration of Python is especially exciting for any Pipeline developer out there, as it allows for a tighter integration of Resolve into existing production pipelines. Pixars [OpenTimelineIO](https://github.com/PixarAnimationStudios/OpenTimelineIO) is living proof that there is quite the demand for this kind of stuff!

At the time of writing, the documentation for the new Scripting API is still .. well, there is none yet. Not really. All there is can be accessed via **Help ➔ Developer Documentation** which will open the developer directory of Resolve on your machine. In the *Scripting* subfolder you will find a *README.txt*, that contains all official information currently available regarding scripting. This includes a very crude description of the available API functions. You will also find a bunch of example scripts written in both, Python and Lua.

While I was searching around the web, I was able to collect some helpful information, resources and code examples. If I manage to find more worthwhile information regarding this topic, I will probably update this post.

## Notes

**Python environment setup**

If you are developing for Python don't forget to set up your System / Python environment accordingly. You'll find the most up-to-date details on how to do that in the official readme file from Blackmagic.

**External / File script execution unavailable in free version**

Playing around with the Python API, I was able to access and modify the current project via the Davinci Resolve Console (*Workspace**➔** Console*). However, I was unable to run any Python scripts from an external terminal window, since the resolve object could not be fetched and was always "NoneType" in my case.

``` python
resolve = dvr_script.scriptapp("Resolve")
print type(resolve)
>> <Type 'NoneType'>
```

In my case, the problem seems to be rooted in the fact that I am using the *free* version of Resolve. According to posts in the BMD forum, the free version of Resolve 15 is limited in it's Scripting capabilities. The Resolve console is the only way to execute Python code in the free version.

To make this a bit less of a pain, the BMD User Steeve Vincent [shared a simple Python script](https://forum.blackmagicdesign.com/viewtopic.php?f=12&t=72497#p445423) that sets up the environment for you and reads and executes any Python script file. Still not a great solution for free users, but better than starting with just the console.

Source: <https://forum.blackmagicdesign.com/viewtopic.php?f=12&t=72497#p444196>

## Additional Resolve Scripting Resources

### Video Tutorials

-   **Python:** [Scripting Introduction Tutorial by Igor Ridanovic](https://www.youtube.com/watch?v=p6IeeWr3FOc)

### Repositories / Code Examples

-   **Python:** [API Tests / Experiments by Igor Ridanovic](https://github.com/IgorRidanovic?tab=repositories)
-   **Lua:** [Resolve Scripting Essentials by Greg Bovine](https://www.steakunderwater.com/wesuckless/viewtopic.php?t=2012)

**Last updated:** 3. January 2019
