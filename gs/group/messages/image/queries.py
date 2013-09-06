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
from Products.XWFMailingListManager.queries import MessageQuery
from gs.database import getSession


class ImageQuery(MessageQuery):
    def file_metadata(self, fileId):
        ft = self.fileTable

        statement = ft.select()
        statement.append_whereclause(ft.c.file_id == fileId)

        session = getSession()
        r = session.execute(statement)
        x = r.fetchone()
        retval = {'file_id': x['file_id'],
                  'mime_type': x['mime_type'],
                  'file_name': x['file_name'],
                  'file_size': x['file_size'],
                  'date': x['date'],
                  'post': self.post(x['post_id']),
                  'topic': self.topic(x['topic_id'])}
        return retval

    def file_metadata_in_topic(self, topicId):
        topicId = topicId.encode('utf-8')

        ft = self.fileTable

        statement = ft.select(order_by=ft.c.date)
        statement.append_whereclause(ft.c.topic_id == topicId)

        session = getSession()
        r = session.execute(statement)
        retval = [{'file_id': x['file_id'],
                  'mime_type': x['mime_type'],
                  'file_name': x['file_name'],
                  'file_size': x['file_size'],
                  'date': x['date'],
                  'post': self.post(x['post_id'])} for x in r]

        assert type(retval) == list
        assert retval
        return retval
