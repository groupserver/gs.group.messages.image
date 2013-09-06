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
