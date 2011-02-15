# coding=utf-8
from zope.interface import Interface
from zope.schema  import Int

class IGSImageView(Interface):
    width = Int(title=u'Width',
        description=u'The width of the image',
        default=432)

    height = Int(title=u'Height',
        description=u'The height of the image',
        default=432)
