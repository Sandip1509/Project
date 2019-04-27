function myFunction() {
  document.getElementById("id_name").value="";
  document.getElementById("id_description").value="";
  document.getElementById("id_start_page").value="";
  document.getElementById("id_end_page").value="";
  document.getElementById("id_price").value="";
}


function download(id){
    var ref_no=id
    alert('Thank you for shopping with us! Now your download will start.!! For future download option will be available in Order History.')
    res=confirm('Are you allow to download file ?');
    if(!res)
        alert('you can download your product from Order History.!!')
    else
        window.open("/media/"+ref_no+".pdf");
}


function pay(id) {
    var url='/customer/pay/'
    var ref_no=id
    array = $.makeArray($('tbody tr[id]').map(function() {
        return this.id;
    }));
    ids=JSON.stringify(array)
    $.ajax({
        type : "POST", // http method
        url : url, // the endpoint
        data:{
            "ref_no":ref_no,
            "id" : ids,
            "book_name" : $('input[name=book_name]').val(),
            "csrfmiddlewaretoken" : $('input[name=csrfmiddlewaretoken]').val()
        },
        success : function() {
            window.location.href = "/customer/buy/" + "?ref_no="+ref_no;
//            window.location = "/customer/buy";
//           if ($('.download-btn').hasClass("disabled")) {
//               $('.buy-btn').addClass('disabled');
//               $('.download-btn').removeClass('disabled');
//            }
//            alert("Thank you  for shopping with us! Your EBook is  ready to download.")
        },
    });
};



function addToCart(clicked_id,name) {
    pk=clicked_id
    var url='/shopping_cart/add-to-cart/'+pk+'/'
    $.ajax({
        type : "POST", // http method
        url : '/shopping_cart/add-to-cart/'+pk+'/', // the endpoint
        data:{
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success : function() {
           if (document.getElementById(pk)) {
             document.getElementById(pk).setAttribute("disabled","disabled");
            }
           alert(name+' successfully added to Cart!');
        },
    });
};



function orderDelete(clicked_id) {
    var pk=clicked_id
    var url='/customer/'+pk+'/orderdelete/'
    $.ajax({
        type : "POST", // http method
        url : url, // the endpoint
        data:{
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success : function() {

        },
    });
};


$(document).ready(function(){
$('.upload-btn').click(function(){
$('#fileUpload').toggle(500);
});
});

var array
$(document).ready(function(request){
    $("#tableID").delegate('button.up','click', function(e) {
        var it = $(this).closest('tr');
        var prev = $(this).closest('tr').prev('tr');
        if(it.attr("id") != $("tbody tr:first").attr("id")){
            it.remove();
            it.insertBefore(prev);
            $(it).find('.up').prop('disabled', false);
            $(it).find('.down').prop('disabled', false);
        }
        if(it.attr("id") == $("tbody tr:first").attr("id")){
            $(prev).find('.up').prop('disabled', false);
            $(it).find('.up').prop('disabled', true);
        }
        if(prev.attr("id") == $("tbody tr:last").attr("id")){
            $(prev).find('.down').prop('disabled', true);
            $(it).find('.down').prop('disabled', false);
        }

    });
    $("#tableID").delegate('button.down','click', function(e) {
        var it = $(this).closest('tr');
        var next = $(this).closest('tr').next('tr');
        if(it.attr("id") != $("tr:last").attr("id")){
            it.remove();
            it.insertAfter(next);
            $(it).find('.up').prop('disabled', false);
            $(it).find('.down').prop('disabled', false);
        }
        if(it.attr("id") == $("tbody tr:last").attr("id")){
            $(next).find('.down').prop('disabled', false);
            $(it).find('.down').prop('disabled', true);
        }
        if(next.attr("id") == $("tbody tr:first").attr("id")){
            $(next).find('.up').prop('disabled', true);
            $(it).find('.up').prop('disabled', false);
        }

    });
});