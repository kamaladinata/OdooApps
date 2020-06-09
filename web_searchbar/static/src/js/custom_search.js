odoo.define("web_searchbar.custom_search", function (require) {
    "use strict";
    require('web.dom_ready');
    $('input[name="search"]').devbridgeAutocomplete({
        serviceUrl: '/document/get_suggest',
        onSelect: function (suggestion) {
            window.location.replace(window.location.origin +
                '/my/hh/' + suggestion.data.id + '?search=' + suggestion.value);
        }
    });
});
