# coding=utf-8
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.XWFFileLibrary2.hidden import FileHidden

class ImageHidden(FileHidden):
    index = ZopeTwoPageTemplateFile('browser/templates/imagehidden.pt')
    def __init__(self, context, request):
        request.form['q'] = request.URL
        request.form['f'] = request['imageId']
        FileHidden.__init__(self, context, request)

