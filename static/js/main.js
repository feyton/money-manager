$(document).ready(function () {
    $(".task-completed").change(function (e) {
        if (this.checked) {
            var delete_task = confirm('Are you sure to delete this task')
            if (delete_task == true) {
                var endpoint = $(this).attr('data-url')
                $.ajax({
                    method: 'GET',
                    url: endpoint,
                    success: function (data) {
                        $.notify({
                            // options
                            title: '<b>Task completed<b> ',
                            message: 'Task with ' + data.ref + ' reference code is completed'
                        }, {
                            // settings
                            type: 'info',
                            delay: 5000,
                            allow_dismiss: true,
                            showProgressbar: true,
                        });
                        $("#" + data.ref).hide(1000)

                    },
                    error: function (error_data) {
                        console.log(error_data)
                    }
                })
            } else {
                $(this).prop('checked', !$(this).prop('checked'));
                $.notify({
                    // options
                    message: '<b>Task not deleted<b>'
                }, {
                    // settings
                    type: 'info',
                    delay: 3000,
                    showProgressbar: true,

                });
            }
        } else {
        }
    })


})