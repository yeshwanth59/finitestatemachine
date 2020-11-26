function validate(event){
console.log("form submission")

    var error = document.getElementById('message')
    console.log(error)
    var message = null
    var values = event.target.elements;
    var name = values.name.value;
    var phone = values.phone.value;
    var phone = values.phone.value;
    var email = values.email.value;
    var password = values.password.value;
    var repassword = values.repassword.value;


    if (!name.trim()){
            message = "name is required"
    }else if(!phone.trim())
    {
                message = "phone number is required"
    }else if(!email.trim())
    {
                message = "email is required"
    }else if(!password.trim())
    {
                message = "password is required"
    }else if(!repassword.trim())
    {
                message = "repassword is required"
    }else if(password.trim() != repassword.trim())
    {            message = "password not matched"}

    if (message){
    error.innerHTML = message
    error.hidden = false
    }else{
    error.innerHTML = ""
    error.hidden = true
//    sendEmail(email)
    }
    event.stopPropagation();
    return false
}
//function sendEmail(email){
//     console.log("send email otp on " + email)
//}