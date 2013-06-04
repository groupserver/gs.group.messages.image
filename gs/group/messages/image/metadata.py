# coding=utf-8
from zope.component import createObject
from zope.cachedescriptors.property import Lazy
from queries import ImageQuery


def get_uri_for_scaled(groupInfo, imageId, maxWidth, maxHeight, filename):
    retval = '/groups/%s/files/f/%s/resize/%s/%s/%s' % \
      (groupInfo.id, imageId, maxWidth, maxHeight, filename)
    assert type(retval) in (str, unicode)
    assert retval
    return retval


def img_url(imgId):
    return '/r/img/%s' % imgId


class Metadata(object):
    def __init__(self, context, imageId):
        self.context = context
        self.imageId = imageId

    @Lazy
    def groupInfo(self):
        return createObject('groupserver.GroupInfo', self.context)

    @Lazy
    def fileQuery(self):
        retval = ImageQuery(self.context)
        assert retval
        return retval

    @Lazy
    def imageMetadata(self):
        retval = self.fileQuery.file_metadata(self.imageId)
        return retval

    @Lazy
    def mime(self):
        return self.imageMetadata['mime_type']

    @Lazy
    def topic(self):
        return self.imageMetadata['topic']

    @Lazy
    def topicShortName(self):
        ts = self.topic['subject'].split()
        if len(ts) < 4:
            retval = self.topic['subject']
        else:
            retval = ' '.join(ts[:3]) + '&#8230;'
        assert retval, 'There is no retval'
        return retval

    @Lazy
    def post(self):
        return self.imageMetadata['post']

    @Lazy
    def postURI(self):
        u = '{0}/messages/post/{1}'
        retval = u.format(self.groupInfo.relativeURL, self.post['post_id'])
        return retval

    @Lazy
    def images_in_topic(self):
        topicId = self.imageMetadata['topic']['topic_id']
        files = self.fileQuery.file_metadata_in_topic(topicId)
        retval = [f for f in files if 'image' in f['mime_type']]
        for f in retval:
            iid = f['file_id']
            fn = f['file_name']
            f['icon_uri'] = get_uri_for_scaled(self.groupInfo, iid, 27, 27, fn)
        return retval

    @Lazy
    def prevImage(self):
        files = self.images_in_topic
        ids = [f['file_id'] for f in files]
        prevs = files[:ids.index(self.imageMetadata['file_id'])]
        retval = prevs and prevs[-1] or None
        return retval

    @Lazy
    def prevURI(self):
        return (self.prevImage and img_url(self.prevImage['file_id'])) or ''

    @Lazy
    def nextImage(self):
        files = self.images_in_topic
        ids = [f['file_id'] for f in files]
        nexts = files[ids.index(self.imageMetadata['file_id']) + 1:]
        retval = nexts and nexts[0] or None
        return retval

    @Lazy
    def nextURI(self):
        return (self.nextImage and img_url(self.nextImage['file_id'])) or ''

    @Lazy
    def authorInfo(self):
        retval = createObject('groupserver.UserFromId', self.context,
                    self.post['author_id'])
        return retval

    @Lazy
    def date(self):
        return self.post['date']
