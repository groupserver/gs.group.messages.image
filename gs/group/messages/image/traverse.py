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
from zope.component import getMultiAdapter
from gs.group.base.page import GroupPage
from Products.XWFFileLibrary2.error import Hidden
from errors import NoIDError

SUBSYSTEM = 'gs.group.messages.image'
import logging
log = logging.getLogger(SUBSYSTEM)


class GSImageTraversal(GroupPage):
    def __init__(self, context, request):
        GroupPage.__init__(self, context, request)

    def publishTraverse(self, request, name):
        if request.get('imageId', None) is None:
            request['imageId'] = name
        return self

    def __call__(self):
        try:
            retval = getMultiAdapter((self.context, self.request),
                        name="gsimage")()
        except NoIDError, n:  # lint:ok
            retval = getMultiAdapter((self.context, self.request),
                        name="gsimage400")()
        except Hidden, h:  # lint:ok
            retval = getMultiAdapter((self.context, self.request),
                                        name="image_hidden.html")()
        return retval
