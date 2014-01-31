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
from zope.contentprovider.interfaces import IContentProvider
from zope.schema import Int, ASCIILine, TextLine


class IGSGroupImageABC(IContentProvider):

    fileId = ASCIILine(title='File Identifier',
                description='The identifier for the image.',
                required=True)

    alt = TextLine(title='Alt Text',
                description='The alternate text for the image.',
                required=False)


class IGSGroupImage(IGSGroupImageABC):
    width = Int(
        title='Width',
        description='The width of the image, in pixels.',
        required=False,
        default=50)  # FIXME: use gs.config

    height = Int(
        title='Height',
        description='The height of the image, in pixels.',
        required=False,
        default=70)  # FIXME: use gs.config

    pageTemplateFileName = ASCIILine(
        title="Page Template File Name",
        description='The name of the ZPT file that is used to render the '
                    'image.',
        required=False,
        default="browser/templates/image.pt".encode('ascii', 'ignore'))


class IGSSquareGroupImage(IGSGroupImage):

    squarePageTemplateFileName = ASCIILine(
        title="Page Template File Name",
        description='The name of the ZPT file that is used to render the '
                    'square image.',
        required=False,
        default="browser/templates/squareimage.pt".encode('ascii', 'ignore'))

    size = Int(
        title='Size',
        description='The width and height of the image, in pixels.',
        required=False,
        default=50)  # FIXME: use gs.config
