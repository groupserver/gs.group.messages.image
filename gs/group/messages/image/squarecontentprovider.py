# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from zope.cachedescriptors.property import Lazy
from zope.pagetemplate.pagetemplatefile import PageTemplateFile
from zope.publisher.interfaces import NotFound
from gs.image import GSSquareImage
from contentprovider import ImageContentProvider


class SquareImageContentProvider(ImageContentProvider):

    def __init__(self, context, request, view):
        super(SquareImageContentProvider, self).__init__(context, request, view)

    def update(self):
        super(SquareImageContentProvider, self).update()
        self.pageTemplate = PageTemplateFile(self.squarePageTemplateFileName)

    @Lazy
    def resizeNeeded(self):
        retval = int(self.size) != self.origImg.width != self.origImg.height
        return retval

    @Lazy
    def origImg(self):
        virtualFileArchive = getattr(self.context, 'files')
        image = virtualFileArchive.get_file_by_id(self.fileId)
        if image is None:
            raise NotFound(virtualFileArchive, self.fileId, self.request)
        data = str(image)
        retval = GSSquareImage(data)
        return retval

    @Lazy
    def smallImage(self):
        if self.resizeNeeded:
            retval = self.origImg.get_resized(int(self.size))
        else:
            retval = self.origImg
        return retval

    def resize_link(self):
        r = '{fileLink}/square/{size}'
        retval = r.format(fileLink=self.file_link(), size=self.size)
        return retval
