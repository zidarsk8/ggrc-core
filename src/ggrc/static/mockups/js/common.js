$(document).ready(function(){
  
  $('[rel=tooltip]').tooltip();
  
  $('.lhs-holder').css('height', 100 + '%');
  $('.inner-nav').css('height', 100 + '%');
  $('.object-area').css('height', 100 + '%');
  
  $('body').on('click', '.info-expand a', function() {
    var $this = $(this),
        $show_hide = $this.closest('.row-fluid').next('.hidden-fields-area');
    
    if($this.hasClass("active")) {
      $show_hide.slideUp('fast');
      $this.removeClass("active");
    } else {
      $show_hide.slideDown('fast');
      $this.addClass("active");
    }
    
    return false;
    
  });

});