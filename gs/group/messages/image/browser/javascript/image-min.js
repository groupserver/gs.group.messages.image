// Copyright (c) 2013 OnlineGroups.net and Contributors.All Rights Reserved. This software is subject to the provisions of the Zope Public License, Version 2.1 (ZPL).
jQuery.noConflict();function gs_group_messages_image(){var a=true;jQuery(".gs-content-js-share").each(function(){a=Boolean(jQuery(this).attr("public"));
shareWidget=GSShareBox(this,a);shareWidget.init()})}jQuery(window).load(function(){gsJsLoader.with_module("/++resource++gs-content-js-sharebox-20130305.js",gs_group_messages_image)
});