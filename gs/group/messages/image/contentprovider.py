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

        self.finalSize = self.get_final_size()
        self.finalWidth = self.finalSize[0]
        self.finalHeight = self.finalSize[1]
        self.imageUrl = self.get_image_url()
        self.image = self.smallImage if self.resizeNeeded else self.origImg

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

    def embedded_image(self):
        d = b64encode(self.smallImage.data)
        r = 'data:{mediatype};base64,{data}'
        retval = r.format(mediatype=self.smallImage.contentType, data=d)
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

    def get_image_url(self):
        if self.smallImage.getSize() < 1023:
            retval = self.embedded_image()
        elif self.resizeNeeded:
            retval = self.resize_link()
        else:
            retval = self.file_link()
        return retval
