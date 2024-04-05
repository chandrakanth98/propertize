// Used in: maintenance.html
window.onload = function() {
    var urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('query') || urlParams.has('status')) {
        $('#collapseRequests').collapse('show');
    }
};
