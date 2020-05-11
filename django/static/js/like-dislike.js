
$(document).ready(function () {
    $('#like').on('click', function (e) {
        e.preventDefault()
        var like = 'like';
        var post_id = $('#post-id').attr('data-id');
        // console.log(post_id);
        data = {
            post_id: post_id,
            like: like
        }

        $.ajax({
            type: "GET",
            url: "/user-reaction/",
            dataType: "json",
            data: data,
            success: function (data) {
                $('#liked').html(data.likes + ' ' + '<i class="far fa-heart heart-like" aria-hidden="true">' + '</i>')
                $('#disliked').html(data.dislikes + ' ' + '<i class="far fa-heart heart-dislike" aria-hidden="true">' + '</i>')

            }
        })
    })
});

$(document).ready(function () {
    $('#dislike').on('click', function (e) {
        e.preventDefault()
        var dislike = 'dislike';
        var post_id = $('#post-id').attr('data-id')
        
        data = {
            post_id: post_id,
            dislike: dislike
        }

        $.ajax({
            type: "GET",
            url: "/user-reaction/",
            dataType: "json",
            data: data,
            success: function (data) {
                $('#liked').html(data.likes + ' ' + '<i class="far fa-heart heart-like" aria-hidden="true">' + '</i>')
                $('#disliked').html(data.dislikes + ' ' + '<i class="far fa-heart heart-dislike" aria-hidden="true">' + '</i>')
            }
        })
    })
})



