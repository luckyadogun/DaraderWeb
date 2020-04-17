$(document).ready(function(){
    $(".lnr-heart").click(function(e){
        e.preventDefault();
        var propertyID = $(this).attr("value");

        $.ajax({
            type: "POST",
            url: "ajax/bookmark",
            dataType: "JSON",
            data: {
                propertyID: propertyID,
                csrfmiddlewaretoken: csrfToken,
            },
            success: function(response){
                var result = response['result'];
                if(result == "Success!"){
                    location.reload();
                }else if(result == "Already Bookmarked!"){
                    alert(result);                    
                }else{
                    $("#user-login-popup").modal("show");
                };
            },
            error: function(response){
                var result = response["result"];                       
                alert("Error! Something went wrong!");
            }
        });
    });
});