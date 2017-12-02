if (window.console) console.log('5oo');
$('#cardcolumns').removeClass('card-columns');
$('#ul-body').removeClass('grid').addClass('list');
$(function() {
$('a').click(function(e) {
 if($(this).hasClass('list')) {
     $('#cardcolumns').removeClass('card-columns');
     $('#ul-body').removeClass('grid').addClass('list');
 }
 else if ($(this).hasClass('grid')) {
     $('#cardcolumns').addClass('card-columns');
     $('#ul-body').removeClass('list').addClass('grid');
 }
});
});

$(document).ready(function() {


  $(".likepost").click(function(){

    var postid = $(this).attr("id");
    var csrftoken = $('input[name=csrfmiddlewaretoken]').val();

     $.ajax({
       url:"/post/" + postid + "/like/",
       data: {"csrfmiddlewaretoken": csrftoken },
       type: "POST",
       context: this,
       success : function(result){
         //$(this).addClass("liked");

         $(this).css('color','red');

       }
     });

  });

});



$(document).ready(function() {
 $("#post-in-image").on('keypress',function(e)
                 {  //var code = e.keyCode
                   if($(this).val().length > 255 )
                   {
                         if (e.keyCode == 13)
                         {+
                           e.preventDefault(); }
                       $('#errorDiv').html("invalid text input too long ");
                   }
                   else
                   {
                      $('#errorDiv').empty();
                   }

                   if( $(this).val().length < 2)
                   {
                      if (e.keyCode==13)
                      {e.preventDefault();}
                      $('#errorDiv').html("enter more than 2 characters ");}

                     });


  });


$(document).ready(function() {
  $("#txt_in_modal").on('keypress',function(e)
                   {  //var code = e.keyCode
                     var btnpost= document.getElementById("postbtn_modal_id")
                     if($(this).val().length > 255)
                     {
                        btnpost.disabled = true;
                         $('#errorDiv_modal').html("your text is too long ");
                         if (e.keyCode == 13 )
                         {    e.preventDefault();
                            $('#errorDiv_modal').html("your text is too long ");
                         }

                     }
                     else
                     {
                       $('#errorDiv_modal').empty();
                        btnpost.disabled=false;

                     }

                  if( $(this).val().length < 1)
                  {
                       if (e.keyCode==13)
                     {e.preventDefault();
                      $('#errorDiv_modal').html("enter more than 1 characters ");}}

                   });
  });
