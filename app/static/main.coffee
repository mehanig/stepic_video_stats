$ ->
  $(".list-element-top-block").click ->
    $(@).parent(@).find(".list-actions-menu").toggleClass("hidden")

  $('.set-yes-status, .set-no-status').click ->
    obj = $(@).closest("ul").attr("id")
    to_update = $(@).closest(".list-group-item").find(".list-element-top-block").find(".video-status")
    is_update = $(@).hasClass("set-yes-status")
    to_hide = $(@).closest(".list-actions-menu")
    $.ajax {
      type: "POST"
      url: "/update"
      dataType: 'json'
      success: (response) ->
        console.log response.html
        to_update.html('UPDATED')
        to_hide.toggleClass("hidden")

      error:(response) ->

      data: {name: obj, is_update: +is_update}
    }