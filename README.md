SCROLLEMU
=========

**scrollemu** is a simple utility that allows you to scroll by holding down a
keyboard modifier key and move your mouse cursor. This is especially nice if
you use a trackball or a pointing stick, but it works for all pointing devices.

I quickly put this script together to make it easier to scroll with my
trackball. It works well on my system without any noticeable impacts on
performance. Your mileage may vary.


Requirements
------------

* Python 3 or 2
* [pynput]

The script should work on all major platforms (Linux with Xorg, Windows,
macOS) but has only been tested on Linux. Wayland is currently not supported.

[pynput]: https://pypi.org/project/pynput/


Install
-------

There is no special install procedure. Simply clone the Git repository:

    git clone https://github.com/hanschen/scrollemu.git

and run the `scrollemu.py` script inside the cloned directory.
Optionally, you can add the `scrollemu` directory to your ``PATH``.


Usage
-----

    scrollemu.py

The script will run until killed. If you find that it works well, you can add
`scrollemu.py` to autostart.


Options
-------

Take a look at the top of the `scrollemu.py` script. In particular, you may
want to change the `SCROLL_KEY` and `SENSITIVITY` options.

If scrolling acts weird, try to disable `ACCELERATION`.


Known issues and future plans
-----------------------------

**Keyboard key is still interpreted as held down.**
This is an issue if e.g. Ctrl is used as the scroll key, as many applications
bind Ctrl+scroll to zoom in/out.

**Mouse cursor flickers when scrolling.**
No idea how to solve this issue, any solutions would be greatly appreciated.

The current script works well for my needs and I don't plan to put much effort
into updating it further. With that said, [pull requests] are always welcome!

[pull requests]: https://github.com/hanschen/scrollemu/pulls


Contact
-------

Author: Hans Chen (contact@hanschen.org)

Website: https://github.com/hanschen/scrollemu
