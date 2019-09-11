function getURLfromURL() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return decodeURIComponent(vars['url']);
}

$(document).ready(function(){
    $("#login_link").attr("href", getURLfromURL());
});