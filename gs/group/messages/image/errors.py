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
from __future__ import unicode_literals
from urllib import quote
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.core import to_ascii
from gs.errormesg.baseerror import BaseErrorPage


class NoIDError(Exception):
    pass


class ImageNoID(BaseErrorPage):
    fileName = 'browser/templates/noid.pt'
    index = ZopeTwoPageTemplateFile(fileName)

    def __init__(self, context, request):
        BaseErrorPage.__init__(self, context, request)
        m = 'Hi! I tried to view an image using the link link %s but '\
            'I saw an Image ID Missing page. I tried... but it '\
            'did not help.' % request.URL
        self.message = quote(m)

    def __call__(self, *args, **kw):
        self.request.response.setHeader(to_ascii('Content-Type'),
                                        to_ascii('text/html; charset=UTF-8'))
        # Return 400: Bad Request
        self.request.response.setStatus(400)
        return self.index(self, *args, **kw)
