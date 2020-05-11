

let button = document.querySelector('.contact-us-button')

// button.addEventListener('click', () => {
//     let email = document.querySelector('#recipient-email').value,
//         theme = document.querySelector('#recipient-theme').value,
//         message = document.querySelector('#recipient-message').value;
//     console.log(email, theme, message)

//     let tooltip = document.createElement('div');
//     tooltip.classList.add('tooltip-for-contact');
//     tooltip.innerHTML = '<p>Спасибо. Ваше сообщение отправлено</p>'
//     if (!document.querySelector('#tooltip-field')) {
//         let tooltip_field = document.createElement('div')
//         tooltip_field.id = 'tooltip-field'
//         document.body.appendChild(tooltip_field)
//     }
//     document.querySelector('#tooltip-field').appendChild(tooltip)
//     setTimeout(() => {
//         tooltip.remove()
//     }, 5000)
    
    
// })


$(document).ready(function() {
    $('.contact-us-button').click((e) => {
        e.preventDefault();
        var email = $('#recipient-email').val()
        let theme = $('#recipient-theme').val()
        let message = $('#recipient-message').val()
        console.log(email)

        data = {
            'email_from_ajax': email,
            'theme_from_ajax': theme,
            'message_from_ajax': message
        }
        
        $.ajax({
            url: '/contact/',
            type: 'GET',
            data: data,
            dataTYpe: 'json',
            success: function () {
                let tooltip = document.createElement('div');
                tooltip.classList.add('tooltip-for-contact');
                tooltip.innerHTML = '<p>Спасибо. Ваше сообщение отправлено</p>'
                if (!document.querySelector('#tooltip-field')) {
                    let tooltip_field = document.createElement('div')
                    tooltip_field.id = 'tooltip-field'
                    document.body.appendChild(tooltip_field)
                }
                document.querySelector('#tooltip-field').appendChild(tooltip)
                setTimeout(() => {
                    tooltip.remove()
                }, 5000)
            }
        })
    })
})