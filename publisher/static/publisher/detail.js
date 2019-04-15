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
    var id = $(".addToCart").attr('id');
    var url='/shopping_cart/add-to-cart/'+id+'/'
    alert(id)
    $.ajax({
        type : "POST", // http method
        url : '/shopping_cart/add-to-cart/'+id+'/', // the endpoint
        data:{
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success : function() {
           if ($('.addtoCart'+id).hasClass("enabled")) {
             $('.addtoCart'+id).addClass('disabled');
            }
            alert('success')
            return document.getElementById(id).value="added";
        },
    });
};