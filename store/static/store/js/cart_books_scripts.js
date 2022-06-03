var cart_book_url = `ws://${window.location.host}/ws/socket-server/store/cart_book/`

const cartBookSocket = new WebSocket(cart_book_url)


if (document.getElementsByClassName('books').length > 0) {
    console.log('We have books element on the page!')
    var books_element = document.getElementsByClassName('books')[0]
    books_in_cart(books_element)
}

if (document.getElementsByClassName('book-detail').length > 0) {
    console.log('We have book detail element on the page!')
    var book_detail_element = document.getElementsByClassName('book-detail')[0]
    book_detail_in_cart(book_detail_element)
}


function add_remove_book_cart(el) {
    var book_id = el.id

    if (el.classList.contains('in_cart')) {
        el.setAttribute('href', '/profile/cart/')
    }

    if (!el.classList.contains('in_cart')) {
        console.log('Send book_id to add book in user cart!')
        cartBookSocket.send(JSON.stringify({
            'message_type': 'add_remove_book_cart',
            'book_id': book_id
        }))
    }

    el.classList.add('in_cart')
    el.getElementsByTagName('span')[0].innerHTML = 'Оформить'
}

function books_in_cart(element) {
    if (cartBookSocket.readyState) {
        var books = element.getElementsByClassName('book')

        cartBookSocket.send(JSON.stringify({
            'message_type': 'books_in_cart'
        }))

        cartBookSocket.onmessage = function (e) {
            var data = JSON.parse(e.data)
            var books_id_set = data['books_id_set']
            for (var i = 0; i < books.length; i++) {
                if (books_id_set.includes(parseInt(books[i].id))) {
                    var buy_btn = books[i].getElementsByClassName('btn-buy-authenticated')[0]
                    buy_btn.classList.add('in_cart')
                    buy_btn.getElementsByTagName('span')[0].innerHTML = 'Оформить'
                }
            }
        }

    }
    else {
        setTimeout(function () {
            books_in_cart(element)
        }, 50)
    }
}

function book_detail_in_cart(element) {
    if (cartBookSocket.readyState) {

        cartBookSocket.send(JSON.stringify({
            'message_type': 'books_in_cart'
        }))

        cartBookSocket.onmessage = function (e) {
            var data = JSON.parse(e.data)
            var books_id_set = data['books_id_set']
            if (books_id_set.includes(parseInt(element.id))) {
                var buy_btn = element.getElementsByClassName('btn-buy-authenticated')[0]
                buy_btn.classList.add('in_cart')
                buy_btn.getElementsByTagName('span')[0].innerHTML = 'Оформить'
            }
        }

    }
    else {
        setTimeout(function () {
            book_detail_in_cart(element)
        }, 50)
    }
}