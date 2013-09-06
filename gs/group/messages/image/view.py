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
from zope.publisher.interfaces import NotFound
from Products.GSGroup.utils import is_public
from Products.XWFFileLibrary2.queries import FileQuery
from Products.XWFFileLibrary2.error import Hidden
from gs.image.image import GSImage
from gs.group.base.page import GroupPage
from errors import NoIDError
from metadata import Metadata, get_uri_for_scaled


class GSImageView(GroupPage):
    def __init__(self, context, request):
        super(GSImageView, self).__init__(context, request)

        self.imageId = imageId = request.get('imageId', None)
        if not self.imageId:
            raise NoIDError('No Image ID')

        self.__topicImages = None

        self.maxWidth = 690  # u on OGN TODO: gs.config
        self.maxHeight = 690  # 34.5u on OGN TODO: gs.config
        self.isPublic = is_public(self.groupInfo.groupObj)

        q = FileQuery()
        if q.file_hidden(imageId):
            raise Hidden(imageId)

    @Lazy
    def metadata(self):
        retval = Metadata(self.context, self.imageId)
        return retval

    @Lazy
    def imageFile(self):
        assert hasattr(self.groupInfo.groupObj, 'files'), \
          'No "files" in %s (%s)' % (self.groupInfo.name, self.groupInfo.id)
        fileLibrary = self.groupInfo.groupObj.files
        retval = fileLibrary.get_file_by_id(self.imageId)
        assert retval, 'Image file not set.'
        return retval

    @Lazy
    def fullImage(self):
        data = str(self.imageFile)
        retval = GSImage(data)
        assert retval
        return retval

    @Lazy
    def scaledImageURI(self):
        # http://wibble.com/groups/bar/files/f/abc123/resize/500/500/foo.jpg
        retval = get_uri_for_scaled(self.groupInfo, self.imageId,
                    self.maxWidth, self.maxHeight, self.filename)
        assert self.imageId in retval
        return retval

    @Lazy
    def fullImageURI(self):
        # http://wibble.com/groups/bar/files/f/abc123/foo.jpg
        retval = '/groups/%s/files/f/%s/%s' % \
          (self.groupInfo.id, self.imageId, self.filename)
        assert self.imageId in retval
        return retval

    @Lazy
    def filename(self):
        try:
            retval = self.metadata.imageMetadata['file_name']
        except TypeError:
            # --=mpj17=-- If we have a None returned by the query then
            # we have no file. Turn the TypeError (500) into a NotFound
            # (404).
            raise NotFound(self, self.imageId, self.request)
        return retval
