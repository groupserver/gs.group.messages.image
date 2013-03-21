===========================
``gs.group.messages.image``
===========================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The images displayed in a GroupServer group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2013-03-21
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 3.0 New Zealand License`_
  by `OnlineGroups.Net`_.

Introduction
============

This is the code for displaying images that have been posted to a group. It
provides two major components: a `content provider`_ for displaying an
image, and the `image page`_.

Content Provider
================

The content provider ``groupserver.GroupImage`` displays an image that has
been posted to a group. It takes four arguments:

:``fileId``: The file identifier (required).
:``alt``: The alt-text (optional, default is blank).
:``width``: The width of the image, in pixels (option, default is 50).
:``height``: The height of the image, in pixels (option, default is 70).

For example, displaying an image with a maximum size of 100 pixels high and
100 wide::

  <span tal:define="fileId view/imageId; width 100; height 100; alt
                    string:The posted image ${view/filename};"
                    tal:replace="structure
                    provider:groupserver.GroupImage">An image</span>

The image is acquired using the virtual file-archive [#archive]_. The image
is then re-sized by ``gs.image`` [#image]_ in such a way that the original
aspect ratio is kept. The content provider will then produce an ``<img>``
element. Based on the result of the re-sizing the ``src`` attribute will
link to one of three things:

#. The original file (``{group}/files/f/{fileId}``), if no resizing was needed.
#. The re-sized file (``{originalFileLink}/resize/{width}/{height}``) if
   resizing is needed and the image is bigger than 1K.
#. A `data-URI`_ if the image is smaller than 1K.

The `square image`_ content provider also re-sizes, but ensures the image
is square.

Square Image
------------


Image Page
==========

Sharebox JavaScript
-------------------

Error pages
-----------

400:

410:


Resources
=========

- Code repository: https://source.iopen.net/groupserver/gs.group.messages.image
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
.. _Creative Commons Attribution-Share Alike 3.0 New Zealand License:
   http://creativecommons.org/licenses/by-sa/3.0/nz/

.. [#archive] See ``Products.XWFFileLibrary2``
              <https://source.iopen.net/groupserver/Products.XWFFileLibrary2>
.. [#image] See ``gs.image``
            <https://source.iopen.net/groupserver/gs.group.messages.image>
.. _data-URI: http://tools.ietf.org/html/rfc2397

..  LocalWords:  fileId GroupImage Sharebox
