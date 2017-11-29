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
