var comment_url = `ws://${window.location.host}/ws/socket-server/store/comment/`

const commentSocket = new WebSocket(comment_url)


function comment_delete(el) {
    var comment_id = el.id
    var comment_el = document.getElementById(`comment-${comment_id}`)
    console.log(comment_id)

    commentSocket.send(JSON.stringify({
        'message_type': 'comment_delete',
        'comment_id': comment_id
    }))

    el.classList.add('comment-delete')
    comment_el.getElementsByClassName('comment-change')[0].classList.add('comment-delete')

    var comment_text_el = comment_el.getElementsByClassName('comment-text')[0]
    comment_text_el.classList.add('comment-text-delete')
    comment_text_el.innerHTML = 'Комментарий удален пользователем.'
}

function comment_change(el) {
    el.style = 'display: none;'
    var comment_id = el.id
    var comment_el = document.getElementById(`comment-${comment_id}`)
    var comment_text_el = comment_el.getElementsByClassName('comment-text')[0]
    comment_text_el.style = 'display: none;'
    var old_text = comment_text_el.textContent

    var comment_change_form_el = document.createElement('form')
    comment_change_form_el.id = 'comment-change-form'
    comment_change_form_el.innerHTML = 
    `<form>
        <textarea id="comment-change-text">${old_text}</textarea>
        <p class="answer-submit-btn" onclick="confirm_comment_change(this)" id="${comment_id}">Изменить</p>
    </form>`
    comment_text_el.after(comment_change_form_el)
}

function confirm_comment_change(el) {
    var comment_id = el.id
    var comment_el = document.getElementById(`comment-${comment_id}`)
    var comment_text_el = comment_el.getElementsByClassName('comment-text')[0]

    var comment_change_form_el = document.getElementById('comment-change-form')
    comment_change_form_el.style = 'display: none;'

    var old_text = comment_text_el.textContent
    var new_text = document.getElementById('comment-change-text').value

    var comment_change_el = comment_el.getElementsByClassName('comment-change')[0]
    comment_change_el.style = 'display: inline-block;'
    comment_text_el.style = 'display: block;'
    comment_text_el.innerHTML = new_text

    if(old_text != new_text){
        commentSocket.send(JSON.stringify({
            'message_type': 'comment_change',
            'comment_id': comment_id,
            'new_text': new_text
        }))
    }
}

function answer_to_comment(el) {
    if(document.getElementById('answer-form')) {
        document.getElementById('answer-form').remove()
    }
    var comment_id = el.id
    var comment_el = document.getElementById(`comment-${comment_id}`)
    var comment_info_el = comment_el.getElementsByClassName('comment-info')[0]
    var answer_el = comment_info_el.getElementsByClassName('answer')[0]
    
    if(!answer_el.classList.contains('answer-open')) {
        var answer_form_el = document.createElement('div')
        answer_form_el.classList.add('answer-form')
        answer_form_el.id = 'answer-form'
        answer_form_el.innerHTML = 
        `<form>
            <textarea id="user-answer-text" placeholder="Ваш ответ на комментарий пользователя..."></textarea>
            <p class="answer-submit-btn" onclick="send_subcomment(this)" id="${comment_id}">Отправить</p>
        </form>`
        answer_el.after(answer_form_el)
    }
    
    answer_el.classList.toggle('answer-open')
}

function send_subcomment(el) {
    var comment_id = el.id
    var book_id = document.getElementsByClassName('book-detail')[0].id
    var comment_text = document.getElementById('user-answer-text').value
    
    if(comment_text.length > 0) {
        commentSocket.send(JSON.stringify({
            'message_type': 'send_subcomment',
            'book_id': book_id,
            'comment_id': comment_id,
            'comment_text': comment_text
        }))
    }
    document.location.reload()
}

function show_comment(el) {
    var comment_id = el.id.split('-')[3]
    var comment_el = document.getElementById(`comment-${comment_id}`)
    comment_el.classList.add('show-comment')

    setTimeout(function() {
        comment_el.classList.remove('show-comment')
    }, 3000)
    
    const elementCoordinates = comment_el.getBoundingClientRect()
    const windowScroll = window.pageYOffset || document.documentElement.scrollTo
    window.scrollTo({
        top: elementCoordinates.top + windowScroll - 100,
        behavior: "smooth"
    })
}