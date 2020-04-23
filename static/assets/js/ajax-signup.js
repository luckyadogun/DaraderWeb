$(document).ready(function(){
    $("#register-form").submit(function(e){
        e.preventDefault();
        e.stopImmediatePropagation();
        var serializedData = $(this).serialize();

        $.ajax({
            type: "POST",
            url: signupURL,
            dataType: "JSON",
            data: serializedData,
            success: function(response){
                var result = response["result"];
                if(result != "Success"){                            
                    $("#signup-modal").append(
                        `
                        <div class="text-left mt-20">
                            <h5 style="color: rgb(187, 26, 26);">
                                ${result}</h5>
                        </div>`
                    )
                    $("#login-form").effect("shake");                    
                };

                if(result == "Success"){
                    $("#signup-modal").append(
                        `
                        <div class="text-left mt-20">
                            <h5 style="color: blue;">
                                Check your email to activate account</h5>
                        </div>`
                    );                    
                }
            },

        });
        return false;
    });     
}); 