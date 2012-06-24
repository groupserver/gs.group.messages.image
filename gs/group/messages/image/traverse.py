# coding=utf-8
from traceback import format_exc
from zope.component import getMultiAdapter
from zope.location.interfaces import LocationError
from zope.publisher.interfaces import NotFound
from gs.group.base.page import GroupPage
from Products.XWFFileLibrary2.error import Hidden
from errors import NoIDError

SUBSYSTEM = 'gs.group.messages.image'
import logging
log = logging.getLogger(SUBSYSTEM) #@UndefinedVariable

class GSImageTraversal(GroupPage):
    def __init__(self, context, request):
        GroupPage.__init__(self, context, request)
        
    def publishTraverse(self, request, name):
        if request.get('imageId', None) == None:
            request['imageId'] = name
            
        return self
    
    def __call__(self):
        try:
            retval = getMultiAdapter((self.context, self.request),
                        name="gsimage")()
        except NoIDError, n:
            retval = getMultiAdapter((self.context, self.request),
                        name="gsimage400")()
        except Hidden, h:
            retval = getMultiAdapter((self.context, self.request),
                                        name="image_hidden.html")()
        return retval

