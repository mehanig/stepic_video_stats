$ ->
  $('.list-element-top-block').click ->
    $(@).parent(@).find('.list-actions-menu').toggleClass('hidden')