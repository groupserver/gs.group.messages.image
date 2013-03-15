# coding=utf-8
from zope.cachedescriptors.property import Lazy
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.XWFFileLibrary2.hidden import FileHidden
from metadata import Metadata


class ImageHidden(FileHidden):
    index = ZopeTwoPageTemplateFile('browser/templates/imagehidden.pt')

    def __init__(self, context, request):
        request.form['q'] = request.URL
        request.form['f'] = request['imageId']
        FileHidden.__init__(self, context, request)

    @Lazy
    def metadata(self):
        return Metadata(self.context, self.fileId)
