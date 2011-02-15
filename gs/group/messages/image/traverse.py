# coding=utf-8
from traceback import format_exc
from zope.component import getMultiAdapter
from zope.location.interfaces import LocationError
from zope.publisher.interfaces import NotFound
from gs.group.base.page import GroupPage
from errors import NoIDError, NoFileError

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
        except NoFileError, f:
            self.request.form['q'] = self.request.URL
            self.request.form['r'] = self.request.get('HTTP_REFERER','')
            retval = getMultiAdapter((self.context, self.request),
                        name="new_not_found.html")()
        except Exception, e:
            self.request.form['q'] = self.request.URL
            self.request.form['m'] = format_exc()
            log.error(format_exc())
            retval = getMultiAdapter((self.context, self.request),
                        name="new_unexpected_error.html")()
        return retval

