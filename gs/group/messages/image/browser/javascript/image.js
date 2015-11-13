'use strict';
// Support for the image page
//
// Copyright © 2013, 2014 OnlineGroups.net and Contributors.
// All Rights Reserved.
//
// This software is subject to the provisions of the Zope Public License,
// Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
// THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
// WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
// WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
// FOR A PARTICULAR PURPOSE.
//
jQuery.noConflict();

function gs_group_messages_image() {
    var isPublic = true, shareWidget = null;
    jQuery('.gs-content-js-share').each(function() {
        // == '1' is More likely to fail-safe
        isPublic = jQuery(this).data('public') == '1';
        shareWidget = GSShareBox(this, isPublic);
        shareWidget.init();
    });
}

jQuery(window).load(function() {
    gsJsLoader.with_module(
        '/++resource++gs-content-js-sharebox-min-20151112.js',
        gs_group_messages_image);
});
