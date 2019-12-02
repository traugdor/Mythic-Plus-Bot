function getURLfromURL() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    
    return decodeURIComponent(vars['url']);
}

$(document).ready(function(){
    var url = getURLfromURL();
    if (url == "undefined"){
        $('#login_section').attr('hidden', true);
        $('#info_section').attr('hidden', false);
    }
    else {
        $('#login_section').attr('hidden', false);
        $('#info_section').attr('hidden', true);
    }
    $("#login_link").attr("href", getURLfromURL());
});