Changelog
=========

2.3.3 (2015-11-12)
------------------

* Following the changes to the `gs.content.js.sharebox`_ code

.. _gs.content.js.sharebox:
   https://github.com/groupserver/gs.content.js.sharebox

2.3.2 (2015-10-30)
------------------

* Using the `file_size_formatter`` function

2.3.1 (2015-10-15)
------------------

* Following the changes to `gs.group.messages.post.base`_
* Using the ``mailto`` function from `gs.core`_
* Pointing at `GitHub`_ as the canonical repository

.. _GitHub:
   https://github.com/groupserver/gs.group.messages.image
.. _gs.group.messages.post.base:
   https://github.com/groupserver/gs.group.messages.post.base
.. _gs.core:
   https://github.com/groupserver/gs.core

2.3.0 (2014-08-28)
------------------

* Adding the ``srcset`` and ``sizes`` attributes, in order to
  provide responsive images.
* Correctly dropping attributes (particularly for SVG).

2.2.0 (2014-03-28)
------------------

* Switching the JavaScript to *strict mode*.
* Turned some ``assert`` statements into raised errors.

2.1.1 (2014-02-20)
------------------

* Ensuring the headers are ASCII.

2.1.0 (2014-01-31)
------------------

* Handling SVG files better.
* Switching to Unicode literals.

2.0.3 (2013-11-14)
------------------

* Updated the JavaScript to follow the *Share box* code.
* Updated the product meatadata.

2.0.2 (2013-09-06)
------------------

* Dropping the word *Post* from the navigation links.
* Updating the license and copyright metadata.

2.0.1 (2013-06-19)
------------------

* Turned a 500-error into a 404.
* Fixed the short topic-name.
* Added data-icons.

2.0.0 (2013-03-21)
------------------

* Support the new GroupServer layout.
* Updated microformats.
* Moved the JavaScript out to its own file, and minified the
  code.
* Added a content provider for images in a group.
* Added a square-image content provider.
* General code cleanup.


1.1.3 (2012-08-02)
------------------

* Removing the lock, which is not supported by ``infrae.wsgi``.

1.1.2 (2012-06-24)
------------------

* Removing a hack for the error-redirection.

1.1.1 (2012-06-18)
------------------

* Returning a more portable URL.

1.1.0 (2011-05-16)
------------------

* Adding a ``410 (Gone)`` page.
* Adding some metadata to the *Image* page.

1.0.0 (2011-02-18)
------------------

* Initial version.

..  LocalWords:  Changelog
