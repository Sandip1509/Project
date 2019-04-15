function myFunction() {
  document.getElementById("id_name").value="";
  document.getElementById("id_description").value="";
  document.getElementById("id_start_page").value="";
  document.getElementById("id_end_page").value="";
  document.getElementById("id_price").value="";
}
//$(document).ready(function(){
//$('.buy-btn').click(function(){
//   if ($('.download-btn').hasClass("disabled")) {
//       $('.download-btn').addClass('active');
//    }
//});
//});


function buy() {
    $.ajax({
        type : "POST", // http method
        url : '/customer/buy/', // the endpoint

        data:{
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success : function() {
           if ($('.download-btn').hasClass("disabled")) {
             $('.download-btn').removeClass('disabled');
            }
        },
    });
};


function addToCart() {
    var pk = $(".addToCart").attr('pk')
    var url='/shopping_cart/add-to-cart/'+pk+'/'
    alert(pk)
    $.ajax({
        type : "POST", // http method
        url : '/shopping_cart/add-to-cart/'+pk+'/', // the endpoint
        data:{
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success : function() {
           if ($('.addToCart').hasClass("enabled")) {
             $('.addToCart').addClass('disabled');
            }
            alert('success');
        },
    });
};