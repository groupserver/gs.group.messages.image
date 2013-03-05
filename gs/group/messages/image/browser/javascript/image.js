jQuery.noConflict();

function gs_group_messages_image () {
    var isPublic = true;
    jQuery('.gs-content-js-share').each(function () {
        isPublic = Boolean(jQuery(this).attr('public'));
        shareWidget = GSShareBox(this, isPublic);
        shareWidget.init();
    });
}

jQuery(window).load(function(){
    gsJsLoader.with_module('/++resource++gs-content-js-sharebox-20130305.js', 
                           gs_group_messages_image);
});
