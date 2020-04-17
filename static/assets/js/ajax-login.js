$(document).ready(function(){
    $("#login-form").submit(function(e){
        e.preventDefault();
        var serializedData = $(this).serialize();

        $.ajax({
            type: "POST",
            url: loginURL,
            dataType: "JSON",
            data: serializedData,
            success: function(response){
                var result = response["result"];
                if(result == "Success!"){
                    $("#user-login-popup").modal("hide");
                    window.location.href = window.location.href;
                }else{
                    $("#login-modal").prepend(
                        `
                        <div class="text-left mt-20">
                            <h5 style="color: rgb(187, 26, 26);">
                                Invalid email or password</h5>
                        </div>`
                    )
                    $("#login-form").effect("shake");
                }  
            },            
        });
    });
});