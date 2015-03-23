$ ->

  collapseRecords($(@))

  $(".list-element-top-block").click ->
    $(@).parent(@).find(".list-actions-menu").toggleClass("hidden")

  $(".show-same-user-vids").click ->
#    uid = $(@).attr('data-user')
#    elements = $(".same-user-list-element[data-user=#{uid}]")
#    console.log elements.length
    $(".same-user-list-element").toggleClass("hide-list-element")
    $(".same-user-videos-navigation").toggleClass("hide-list-element")

  $('.set-yes-status, .set-no-status, .delete-record').click ->
    obj = $(@).closest(".list-actions-menu").attr("id")
    thisObj = $(@)
    to_update = $(@).closest(".list-group-item").find(".list-element-top-block").find(".video-status")
    is_update = $(@).hasClass("set-yes-status")
    to_hide = $(@).closest(".list-actions-menu")
    action = findAction($(@))
    $.ajax {
      type: "POST"
      url: "/update"
      dataType: 'json'
      success: (response) ->
        console.log response.html
        to_update.html('UPDATED')
        to_hide.toggleClass("hidden")

      error:(response) ->
      data: {name: obj, is_update: +is_update, action:action}
    }


findAction = (obj) ->
  if obj.hasClass('delete-record')
    return "delete"
  return 0

collapseRecords = (obj) ->
  data_list = obj.find('.list-group').each ->
    console.log @

