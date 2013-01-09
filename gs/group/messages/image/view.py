# -*- coding: utf-8 -*-
from zope.publisher.interfaces import NotFound
from zope.cachedescriptors.property import Lazy
from Products.GSGroup.utils import is_public
from gs.image.image import GSImage
from gs.group.base.page import GroupPage
from Products.XWFFileLibrary2.queries import FileQuery
from Products.XWFFileLibrary2.error import Hidden
from errors import NoIDError
from metadata import Metadata, get_uri_for_scaled


class GSImageView(GroupPage):
    def __init__(self, context, request):
        GroupPage.__init__(self, context, request)

        self.imageId = imageId = request.get('imageId', None)
        if not self.imageId:
            raise NoIDError('No Image ID')

        self.__topicImages = None

        # --=mpj17=-- The image pages are optimised to view photographs,
        #   which have a ratio of 3:4.
        self.maxWidth = 639  # u on OGN TODO: gs.config
        self.maxHeight = 852  # 34.5u on OGN TODO: gs.config
        self.isPublic = is_public(self.groupInfo.groupObj)

        q = FileQuery(self.context)
        if q.file_hidden(imageId):
            raise Hidden(imageId)

    @Lazy
    def metadata(self):
        return Metadata(self.context, self.imageId)

    @Lazy
    def imageFile(self):
        assert hasattr(self.groupInfo.groupObj, 'files'), \
          'No "files" in %s (%s)' % (self.groupInfo.name, self.groupInfo.id)
        fileLibrary = self.groupInfo.groupObj.files
        files = fileLibrary.find_files({'id': self.imageId})
        if len(files) < 1:
            raise NotFound(self, self.imageId, self.request)
        retval = files[0].getObject()
        assert retval, 'Image file not set.'
        return retval

    @Lazy
    def fullImage(self):
        retval = GSImage(self.imageFile.data)
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
        # Inspried by the get_file method of the virtual file library.
        title = self.imageFile.getProperty('title', '')
        retval = self.imageFile.getProperty('filename', title).strip()
        return retval
