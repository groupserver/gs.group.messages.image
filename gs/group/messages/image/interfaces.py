# coding=utf-8
from zope.contentprovider.interfaces import IContentProvider
from zope.schema import Int, ASCIILine, TextLine


class IGSGroupImageABC(IContentProvider):

    fileId = ASCIILine(title=u'File Identifier',
                description=u'The identifier for the image.',
                required=True)

    alt = TextLine(title=u'Alt Text',
                description=u'The alternate text for the image.',
                required=False)


class IGSGroupImage(IGSGroupImageABC):
    width = Int(
        title=u'Width',
        description=u'The width of the image, in pixels.',
        required=False,
        default=50)  # FIXME: use gs.config

    height = Int(
        title=u'Height',
        description=u'The height of the image, in pixels.',
        required=False,
        default=70)  # FIXME: use gs.config

    pageTemplateFileName = ASCIILine(
        title=u"Page Template File Name",
        description=u'The name of the ZPT file that is used to render the '
                    u'image.',
        required=False,
        default="browser/templates/image.pt")


class IGSSquareGroupImage(IGSGroupImage):

    squarePageTemplateFileName = ASCIILine(
        title=u"Page Template File Name",
        description=u'The name of the ZPT file that is used to render the '
                    u'square image.',
        required=False,
        default="browser/templates/squareimage.pt")

    size = Int(
        title=u'Size',
        description=u'The width and height of the image, in pixels.',
        required=False,
        default=50)  # FIXME: use gs.config
