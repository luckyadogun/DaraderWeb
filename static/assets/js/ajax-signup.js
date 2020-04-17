$(document).ready(function(){
    $("#register-form").submit(function(e){
        e.preventDefault();
        var serializedData = $(this).serialize();

        $.ajax({
            type: "POST",
            url: "ajax/signup",
            dataType: "JSON",
            data: serializedData,
            success: function(response){
                var result = response["result"];
                if(result == "Failed"){                            
                    $("#signup-modal").append(
                        `
                        <div class="text-left mt-20">
                            <h5 style="color: rgb(187, 26, 26);">
                                Either username or e-mail is unavailable!</h5>
                        </div>`
                    )
                    $("#login-form").effect("shake");
                };

                if(result == "Success"){
                    location.reload();
                }
            },
            error: function(response){
                $("#signup-modal").prepend(
                    `
                    <div class="text-left mt-20">
                        <h5 style="color: rgb(187, 26, 26);">
                            Ooops! Something went wrong!.</h5>
                    </div>`
                    )
                $("#login-form").effect("shake");
            }
     
        });
    });     
}); 