# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import unicode_literals
from base64 import b64encode
from zope.cachedescriptors.property import Lazy
from zope.contentprovider.interfaces import UpdateNotCalled
from zope.pagetemplate.pagetemplatefile import PageTemplateFile
from zope.publisher.interfaces import NotFound
from gs.group.base import GroupContentProvider
from gs.image import GSImage


class ImageContentProvider(GroupContentProvider):
    """The user image."""

    def __init__(self, context, request, view):
        super(ImageContentProvider, self).__init__(context, request, view)
        self.updated = False
        self.pageTemplate = self.image = None

    def update(self):
        self.updated = True
        self.pageTemplate = PageTemplateFile(self.pageTemplateFileName)

        self.finalSize = self.get_final_size()
        self.finalWidth = self.finalSize[0]
        self.finalHeight = self.finalSize[1]
        self.imageUrl = self.get_image_url()
        self.image = self.smallImage if self.resizeNeeded else self.origImg
        # --=mpj17=-- The page template uses self.image.ct, rather than
        # self.image.contentType because it will drop the attribute if it
        # is None, but self.image.contentType is never None, just ''.
        # A similar issue hits self.sizes and self.srcset below
        ct = self.image.contentType
        self.image.ct = ct if ct else None

    def render(self):
        if not self.updated:
            raise UpdateNotCalled
        return self.pageTemplate(view=self)

    def get_final_size(self):
        if self.resizeNeeded:
            retval = self.smallImage.getImageSize()
        else:
            retval = self.origImg.getImageSize()
        return retval

    @Lazy
    def resizeNeeded(self):
        retval = ((int(self.width) < self.origImg.width) or
                  (int(self.height) < self.origImg.height))
        return retval

    @Lazy
    def origImg(self):
        virtualFileArchive = getattr(self.context, 'files')
        image = virtualFileArchive.get_file_by_id(self.fileId)
        if image is None:
            raise NotFound(virtualFileArchive, self.fileId, self.request)
        data = str(image)
        retval = GSImage(data)
        assert retval, 'There is no image'
        return retval

    @Lazy
    def smallImage(self):
        if self.resizeNeeded:
            w = int(self.width)
            h = int(self.height)
            retval = self.origImg.get_resized(w, h)
        else:
            retval = self.origImg
        return retval

    @Lazy
    def sizes(self):
        'The value for the sizes attribute of the image.'
        retval = None  # --=mpj17=-- Deliberately None, not ''
        if self.finalWidth > 0:
            # If we are dealing with something that PIL can scale...
            # To be read as "if the viewport is as big as the image, then
            # show the full image, else scale the image to the size of the
            # viewport."
            r = '(min-width: {0}px) {0}px,\n     (max-width: {1}px) 100vw'
            retval = r.format(self.finalWidth, self.finalWidth-1)
        return retval

    @Lazy
    def srcset(self):
        'The value of the srcset attribute of the image'
        retval = None
        if self.finalWidth > 0:
            # If we are dealing with something that can be scaled by PIL
            sizes = []
            # --=mpj17=-- In theory we can do this in 1px increments, but
            # that would result in too much HTML. Each 100px drop in width
            # equates to a ten-ish kiliobyte reduction in size.
            s = '{0}/resize/'.format(self.file_link())
            for breakpoint in range(self.finalWidth, 100, -100):
                size = '{0}{1}/{1} {1}w'.format(s, breakpoint)
                sizes.append(size)
            retval = ',\n'.join(sizes)
        return retval

    def embedded_image(self):
        d = b64encode(self.smallImage.data)
        r = 'data:{mediatype};base64,{data}'
        retval = r.format(mediatype=self.smallImage.contentType, data=d)
        return retval

    def file_link(self):
        r = '{group}/files/f/{fileId}'
        retval = r.format(group=self.groupInfo.relativeURL,
                          fileId=self.fileId)
        return retval

    def resize_link(self):
        r = '{fileLink}/resize/{width}/{height}'
        retval = r.format(fileLink=self.file_link(), width=self.width,
                          height=self.height)
        return retval

    def get_image_url(self):
        if self.smallImage.getSize() < 1023:
            retval = self.embedded_image()
        elif self.resizeNeeded:
            retval = self.resize_link()
        else:
            retval = self.file_link()
        return retval
