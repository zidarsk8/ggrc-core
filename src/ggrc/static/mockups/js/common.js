$(document).ready(function(){

  $('body').on('click', '.color-trigger', function() {
    var $this = $(this),
        $colorText = $this.closest('.content').find('h2');
    
    if($this.hasClass("clicked")) {
      $colorText.css('color', '#000');
      $this.removeClass("clicked");
    } else {
      $colorText.css('color', '#ff0000');
      $this.addClass("clicked");
    }
    
    return false;
    
  });

});