# -*- coding: utf-8 -*-
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

        self.image = self.get_image()
        self.resizeNeeded = self.get_resize_needed()
        self.s = [int(d) for d in (self.width, self.height)]
        self.shouldEmbed = self.get_should_embed()
        self.finalSize = self.get_final_size()
        self.finalWidth = self.finalSize[0]
        self.finalHeight = self.finalSize[1]

    def get_image(self):
        virtualFileArchive = getattr(self.context, 'files')
        image = virtualFileArchive.get_file_by_id(self.fileId)
        if image is None:
            raise NotFound(virtualFileArchive, self.fileId, self.request)
        data = str(image)
        retval = GSImage(data)
        return retval

    def get_resize_needed(self):
        retval = ((int(self.width) < self.image.width) or
                    (int(self.height) < self.image.height))
        return retval

    def get_should_embed(self):
        m1 = max(self.image.getImageSize())
        m2 = max(self.s)
        retval = min((m1, m2)) < 40
        return retval

    def get_final_size(self):
        if self.resizeNeeded:
            w = int(self.width)
            h = int(self.height)
            smallImage = self.image.get_resized(w, h)
            retval = smallImage.getImageSize()
        else:
            retval = self.image.getImageSize()
        return retval

    def render(self):
        if not self.updated:
            raise UpdateNotCalled
        return self.pageTemplate(view=self)

    @Lazy
    def imageUrl(self):
        if self.shouldEmbed:
            retval = self.embedded_image()
        elif self.resizeNeeded:
            retval = self.resize_link()
        else:
            retval = self.file_link()
        return retval

    def embedded_image(self):
        w = int(self.width)
        h = int(self.height)
        smallImage = self.image.get_resized(w, h)
        d = b64encode(smallImage.data)
        r = 'data:{mediatype};base64,{data}'
        retval = r.format(mediatype=smallImage.contentType, data=d)
        return retval

    def file_link(self):
        r = '{group}/files/f/{fileId}'
        retval = r.format(group=self.groupInfo.relativeURL, fileId=self.fileId)
        return retval

    def resize_link(self):
        r = '{fileLink}/resize/{width}/{height}'
        retval = r.format(fileLink=self.file_link(), width=self.width,
                            height=self.height)
        return retval
