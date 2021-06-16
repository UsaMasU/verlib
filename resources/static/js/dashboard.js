const SESSION_STATE = 'search';

$(document).ready(function(){
    if (sessionStorage.getItem(SESSION_STATE) == null || sessionStorage.getItem(SESSION_STATE) == undefined){
        sessionStorage.setItem(SESSION_STATE, tree = JSON.stringify({'status':'', 'text':''}));
    }
    else {
        search = JSON.parse(sessionStorage.getItem(SESSION_STATE));
        if(search['status'] == 'active'){
           $(".showSearch").addClass("active");
           $("#searchBtn .btn").addClass("btn-info");
           $("input.form-control.search-slt")[0].value = search['text']
        }
    }

    $("#searchBtn").click(function(){
        let status;
        search = JSON.parse(sessionStorage.getItem(SESSION_STATE));
        $(".showSearch").toggleClass("active");
        $("#searchBtn .btn").toggleClass("btn-info");
        $(".showSearch").hasClass("active") ? status = 'active' : status = 'hide';
        $("input.form-control.search-slt")[0].value = search['text']
        sessionStorage.setItem(SESSION_STATE, JSON.stringify({'status': status, 'text': search['text']}));
    });

    $("button.btn.showSearch").click(function(event){
        sessionStorage.setItem(SESSION_STATE, JSON.stringify({'status': 'active', 'text': $("input.form-control.search-slt")[0].value}));
    });

});
