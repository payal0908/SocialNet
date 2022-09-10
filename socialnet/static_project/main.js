// dropdown 
$('.ui.dropdown')
  .dropdown()
;

// message alert
$('.message .close')
  .on('click', function() {
    $(this)
      .closest('.message')
      .transition('fade')
    ;
  })
;