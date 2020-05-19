
AppendNameAuthorToForm()

function AppendNameAuthorToForm() {
    /* Функция получает имя автора и подставляет в форму ответа */
    let for_reply_comment = document.querySelectorAll('.for-reply-comment')
    let reply_comments = document.querySelectorAll('.reply-comment')
    
    for_reply_comment.forEach((item, i) => {
    
        item.addEventListener('click', function () {
            
                let author = item.dataset.name
                let reply_name_authr = document.querySelector('#your-name-reply'); // куда будет поставляться имя для ответа
                console.log(author)
    
                document.querySelector('.form-for-comment-reply').style.display = '';
                let form = document.querySelector('.form-for-comment-reply');

                form.scrollIntoView(false);
    
                document.querySelector('.input-hidden').value = item.dataset.id;
                document.querySelector('.hidden-reply-to').value = author;
                
                let text_body_reply = item.parentElement
                document.querySelector('.message-reply-to').value = text_body_reply.querySelector('div.text>p').textContent;
                
                reply_name_authr.innerHTML = `Ваш ответ для ${author}`;
                form.querySelector('#contactcomment').innerText = `${author}, `;
                document.querySelector('.default-comment-form').style.display = 'none';
                document.querySelector('strong.link-reply').textContent = `${author}`;
     
            });
    });
};


ShowHideCurrentReplies()

function ShowHideCurrentReplies() {
    let basic_comments = document.getElementsByClassName('basic-comment')
    for (let i = 0; i < basic_comments.length; i++) {
        const element = basic_comments[i];
        
        if (element.childNodes[9].className == 'theme-btn reply-btn-author') {
            let buttn = element.childNodes[9];
    
            buttn.addEventListener('click', function (event) {
                event.preventDefault();
                let trgt = event.target;
    
                let nxt_el = trgt.closest('.comments-and-reply');
                let replies = nxt_el.getElementsByClassName('reply-comment');
                for (let j = 0; j < replies.length; j++) {
                    if (replies[j].style.display == 'none') {
                        replies[j].style.display = '';
                        buttn.textContent = `скрыть ответы (${replies.length})`;
                        
                    } else {
                        replies[j].style.display = 'none';
                        buttn.textContent = `показать ответы (${replies.length})`;
                    }              
                }
            })
            
        }
    }


};




// ShowHideAllComments()

// function ShowHideAllComments() {
//     let button = document.querySelector('#comments-area-id')
//     button.addEventListener('click', (e) => {
//         e.preventDefault()
//         let a = document.querySelectorAll('.comments-and-reply')
//         a.forEach(item => {
//             if (item.style.display == '') {
//                 // item.style.display = 'none'
//                 setTimeout(() => item.style.display = 'none', 100)
//             } else {
//                 // item.style.display = ''
//                 setTimeout(() => item.style.display = '', 100)
//             }
            
//         })
//     })
// };

// плавно скрыть показать все комментарии
$(document).ready(function(){
    var btn = $("#comments-area-id")
    btn.click((e) => {
        e.preventDefault();
        // let all_comments = $('.comments-and-reply')
        
        // $('.comments-and-reply').each(function(index, value) {
        //     // $(this).toggle('normal');
        //     $(this).toggle();
                
        // });
        
    });
    
});

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



// $(function(){
//     $('.show-more').click(function(e){
//         e.preventDefault();
//         $('.comments-and-reply').toggleClass('open');
//     });
// });


ShowFiveNextComments()

function ShowFiveNextComments() {
    if (document.querySelector('.show-more')) {
    document.querySelector('.show-more').addEventListener('click', (e) => {
        e.preventDefault();
        let blockComment = document.querySelectorAll('.comments-and-reply:nth-child(n+4)')
        console.log(blockComment.length)
        for (let i = 0; i < blockComment.length; i++) {
            blockComment[i].classList.add('open')
            // const element = blockComment[i];
            document.querySelector('.show-more').style.display = 'none'
            
        }
        
    })
}
}

ShowButton()

function ShowButton() {
    let blockComment = document.querySelectorAll('.comments-and-reply')
    if (document.querySelector('.show-more') && blockComment.length > 4) {
        document.querySelector('.show-more').style.display = ''
    } 
    else {
        document.querySelector('.show-more').style.display = 'none'
    }
    
}

// $(function () {
//     x=3;
//     $('.comments-and-reply').slice(0, 3).show();
//     $('.show-more').on('click', function (e) {
//         e.preventDefault();
//         x = x+5;
//         $('.comments-and-reply').slice(0, x).slideDown();
//     });
// });



// showMore()

// var numberShown = 4;
// function showMore() {
//     document.querySelector('.show-more').addEventListener('click', (e) => {
//         e.preventDefault();
//         numberShown += 5;
//         for(var i = 0; i < numberShown; ++i) {

//             document.querySelectorAll(".comments-and-reply")[i].style.display = "block";
//             if (document.querySelectorAll(".comments-and-reply").length > numberShown) {
//                 document.querySelector('.show-more').style.display = 'none'
//             }
//         }

   
//     }
// )}