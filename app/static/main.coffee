$ ->
  collapseRecords($(@))

  $.get('hiddenTemplate').done (data) ->
    $(e).after(data) for e in $(".userRecord[is_main = '1']")

  $(".list-element-top-block").click ->
    $(@).parent(@).find(".list-actions-menu").toggleClass("hidden")

  $(".show-same-user-vids").click ->
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
  obj.find('.list-group').children('.userRecord').toArray().forEach(collapseElement)


#TODO: Please, refactor it later. =(
collapseElement = (element, index, array) ->
  if index > 0 and  $(element).attr('data-user') == $(array[index-1]).attr('data-user')
    if !!$(array[index-1]).attr('is_main') and not !!$(array[index-1]).attr('not-main')
      $(array[index-1]).attr('data-contain-hidden', parseInt($(array[index-1]).attr('data-contain-hidden'))+1)
      $(element).attr('not-main','1').attr('is-from', index-1)
    else if !!$(array[index-1]).attr('not-main')
      is_from = parseInt($(array[index-1]).attr('is-from'))
      $(element).attr('not-main','1').attr('is-from', is_from)
      $(array[is_from]).attr('data-contain-hidden', parseInt($(array[is_from]).attr('data-contain-hidden'))+1)
  else
    $(element).attr('is_main','1')
    $(element).attr('data-contain-hidden', '0')