$(document).ready(function(){
    $(".lnr-heart").click(function(e){
        e.preventDefault();
        var propertyID = $(this).attr("value");

        console.log(bookmarkURL);

        $.ajax({
            type: "POST",
            url: bookmarkURL,
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
        return false;
    });
});