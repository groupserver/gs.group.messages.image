# coding=utf-8
from zope.component import createObject
from zope.publisher.interfaces import IPublishTraverse, NotFound
from zope.interface import implements
from zope.cachedescriptors.property import Lazy
from Products.GSGroup.utils import is_public
from gs.image.image import GSImage
from gs.group.base.page import GroupPage
from Products.XWFFileLibrary2.queries import FileQuery
from Products.XWFFileLibrary2.error import Hidden
from queries import ImageQuery
from errors import NoIDError

class GSImageView(GroupPage):
    def __init__(self, context, request):
        GroupPage.__init__(self, context, request)

        self.imageId = imageId = request.get('imageId', None)
        if not self.imageId:
            raise NoIDError('No Image ID')
        
        self.__topicImages = None
        
        # --=mpj17=-- The image pages are optimised to view photographs,
        #   which have a ratio of 4:3.
        self.maxWidth = 598  # 46.0u on OGN
        self.maxHeight = 449 # 34.5u on OGN
        self.isPublic = is_public(self.groupInfo.groupObj)

        da = self.context.zsqlalchemy
        q = FileQuery(self.context, da)
        if q.file_hidden(imageId):
            raise Hidden(imageId)
                
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
    def fileQuery(self):
        da = self.context.zsqlalchemy 
        assert da, 'No data-adaptor found'
        retval = ImageQuery(self.context, da)
        assert retval
        return retval

    @Lazy
    def scaledImageURI(self):
        # http://wibble.com/groups/bar/files/f/abc123/resize/500/500/foo.jpg
        retval = self.get_uri_for_scaled(self.imageId, self.maxWidth,
                                         self.maxHeight, self.filename)
        assert self.imageId in retval
        return retval
    
    def get_uri_for_scaled(self, imageId, maxWidth, maxHeight, filename):
        retval = '%s/files/f/%s/resize/%s/%s/%s' % \
          (self.groupInfo.url, imageId, maxWidth, maxHeight, filename)
        # assert type(retval) == str
        assert retval
        return retval
    
    @Lazy
    def fullImageURI(self):
        # http://wibble.com/groups/bar/files/f/abc123/foo.jpg
        retval = '%s/files/f/%s/%s' % \
          (self.groupInfo.url, self.imageId, self.filename)
        assert self.imageId in retval
        return retval

    @Lazy
    def filename(self):
        # Inspried by the get_file method of the virtual file library.
        title = self.imageFile.getProperty('title', '')
        retval = self.imageFile.getProperty('filename', title).strip()
        return retval

    @Lazy
    def topic(self):
        retval = self.imageMetadata['topic']
        assert type(retval) == dict
        assert retval
        return retval

    @Lazy
    def post(self):
        retval = self.imageMetadata['post']
        assert type(retval) == dict
        assert retval
        return retval
        
    @Lazy
    def authorInfo(self):
        authorId = self.post['author_id']
        self.__authorInfo = createObject('groupserver.UserFromId',
                                         self.context, authorId)
        return retval
        
    @Lazy
    def imageMetadata(self):
        retval = self.fileQuery.file_metadata(self.imageId)
        return retval

    def images_in_topic(self):
        if self.__topicImages == None:
            topicId = self.imageMetadata['topic']['topic_id']
            files = self.fileQuery.file_metadata_in_topic(topicId)
            self.__topicImages = [f for f in files 
                                  if 'image' in f['mime_type']]
            for f in self.__topicImages:
                iid = f['file_id']
                fn = f['file_name']
                f['icon_uri'] = self.get_uri_for_scaled(iid, 27, 27, fn)

        retval = self.__topicImages
        assert type(retval) == list
        assert retval
        return retval
    
    @Lazy
    def prevImage(self):
        files = self.images_in_topic()
        ids = [f['file_id'] for f in files]
        prevs = files[:ids.index(self.imageMetadata['file_id'])]
        retval = prevs and prevs[-1] or None
        return retval

    @Lazy
    def nextImage(self):
        files = self.images_in_topic()
        ids = [f['file_id'] for f in files]
        nexts = files[ids.index(self.imageMetadata['file_id']) + 1:]
        retval = nexts and nexts[0] or None
        return retval

