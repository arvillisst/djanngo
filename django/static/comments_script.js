
let for_reply_comment = document.querySelectorAll('.for-reply-comment')

let reply_comments = document.querySelectorAll('.reply-comment')

for_reply_comment.forEach((item, i) => {
    // console.log(item.dataset)
    // console.log(item.attributes[0])

    item.addEventListener('click', function () {
        
            let author = item.dataset.name
            let reply_name_authr = document.querySelector('#your-name-reply'); // куда будет поставляться имя для ответа
            console.log(author)

            document.querySelector('.form-for-comment-reply').style.display = '';
            let form = document.querySelector('.form-for-comment-reply');

            document.querySelector('.input-hidden').value = item.dataset.id;
            document.querySelector('.hidden-reply-to').value = author;
            // .split(' ')[0]
            let text_body_reply = item.parentElement
            document.querySelector('.message-reply-to').value = text_body_reply.querySelector('div.text>p').textContent;
            let txt = text_body_reply.querySelector('div.text>p').textContent
            let txt_splited = txt.split(',')[0]
            console.log(txt_splited)
            console.log(txt.substr(txt_splited.length, 200))
            console.log(text_body_reply.querySelector('div.text>p').textContent)

            reply_name_authr.innerHTML = `Ваш ответ для ${author}`;
            form.querySelector('#contactcomment').innerText = `${author}, `;
            document.querySelector('.default-comment-form').style.display = 'none';
            document.querySelector('strong.link-reply').textContent = `${author}`;
 
        });
});



let basic_comments = document.getElementsByClassName('basic-comment')
for (let i = 0; i < basic_comments.length; i++) {
    const element = basic_comments[i];

    if (element.childNodes[9].className == 'theme-btn reply-btn-author') {
        let buttn = element.childNodes[9]

        buttn.addEventListener('click', function (event) {
            event.preventDefault()
            // console.log(event.target)
            let trgt = event.target

            let nxt_el = trgt.closest('.comments-and-reply')
            let replies = nxt_el.getElementsByClassName('reply-comment')
            for (let j = 0; j < replies.length; j++) {
                if (replies[j].style.display == 'none') {
                    replies[j].style.display = '';
                    buttn.textContent = `скрыть ответы (${replies.length})`
                    
                    let name_reply = replies[j].querySelector('.link-reply')
                    name_reply.addEventListener('mouseover', () => {
                        // console.log(replies[j].querySelector('.link-reply-body').textContent)
                        if (replies[j].querySelector('.link-reply-body').style.display == 'none') {
                            
                            let link_for_hide = replies[j].querySelector('.link-reply-body').style.display = ''
                            setTimeout( () => link_for_hide, 2000);
                        } else {
                            replies[j].querySelector('.link-reply-body').style.display = 'none'
                        }   
                    })

                    name_reply.addEventListener('mouseout', () => {
                        // console.log(replies[j].querySelector('.link-reply-body').textContent)
                        if (replies[j].querySelector('.link-reply-body').style.display == 'none') {
                            
                            let link_for_hide = replies[j].querySelector('.link-reply-body').style.display = ''
                            setTimeout( () => link_for_hide, 2000);
                        } else {
                            replies[j].querySelector('.link-reply-body').style.display = 'none'
                        }   
                    })
                    
                } else {
                    replies[j].style.display = 'none';
                    buttn.textContent = `показать ответы (${replies.length})`
                }              
            }
        })
        
    }
}

// Плавно прокрутить до формы ответа ///
// $(document).ready(function(){
//     $(".for-reply-comment").click(function (e) {
//         e.preventDefault();

//         var link  = $(this).attr('href'),
//             top = $(link).position().top;
//         // console.log($(".for-reply-comment"))
//         console.log(link)
//         $('body, html').animate({scrollTop: top}, 500);
        
//     });
    
// });


// $(document).ready(function() {
//     $('#comments-area-id').click(function(e) {
//         e.preventDefault();
//         $('#1234').toggle();
//     });
    
// });