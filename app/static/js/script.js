// //sortable task list
// $(function() {
//   //add id's to the li elements so after sorting we can save the order in localstorage
//   $( "#sortable>li" ).each(function(index, domEle) { $(domEle).attr('id', 'item_'+index) });
//   $( "#sortable" ).sortable( {
//     placeholder: "ui-state-highlight",
//     update: function(event, ui) {        
//       localStorage.setItem("sorted",  $("#sortable").sortable("toArray"));
//     }
//   });
//   restoreSorted();
// });

// function restoreSorted() {
//     var sorted = localStorage["sorted"];      
//     if(sorted == undefined) return;
//     var elements = $("#sortable");
//     var sortedArr = sorted.split(",");
//     for (var i = 0; i < sortedArr.length; i++) {
//         var el = elements.find("#" + sortedArr[i]);
//         $("#sortable").append(el);
//     };
// }

//ajax create task
$(document).ready(function() {
    $('#create_task').on('submit', function(event) {
        $.ajax( {
            url: 'create_task',
            type: 'POST',
            data: $(this).serialize(),
            success: function(data) {
                    console.log(data);
                    var html = '<li class="ui-state-default mb-4 pb-4"><div class="row"><div class="col-auto">';
                    html += 'id: '+data.task_id+'</br>';
                    html += 'task: '+data.task_name+'</br>';
                    html += 'due date: '+data.task_due+'</br>';
                    html += 'remind on: '+data.task_remind+'</br>';
                    html += '</div></div>';
                    
                    html += '<div class="row my-2"><div class="col-auto">';
                    html += '<form action="delete_task/'+data.task_id+'", method="POST"><input class="btn btn-outline-dark btn-sm" id="delete" name="delete" type="submit" value="delete"></input></form>';
                    html += '</div></div></li>';
                    $('#sortable').prepend(html);
                    $('#notask').hide();
                    $('#create_task')[0].reset();
                    setTimeout(function(){ alert("task created!"); }, 300);
            },
            error: function (data) {
                console.error('Error:', data);
                alert("creating task failed!"); 
            }
        });
        event.preventDefault();
    });
  
    //ajax delete task
    // $('.delete_task').on('click', function(event) {
    //     var taskId = $(this).data('task_id')
    //     $.ajax( {
    //         url: 'delete_task/' + taskId,
    //         type: 'POST',
    //         success: function(data) {
    //             console.log(data);
    //             $('#'+taskId).hide();
    //             setTimeout(function(){ alert("task deleted!"); }, 300);
    //         },
    //         error: function (data) {
    //             console.error('Error:', data);
    //             alert("deleting task failed!"); 
    //         }
    //     });
    //     event.preventDefault();
    // });

    //inject our CSRF token into our AJAX request.
    $.ajaxSetup( {
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", "{{ form.csrf_token._value() }}")
            }
        }
    });
});