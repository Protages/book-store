var book_favourites_url = `ws://${window.location.host}/ws/socket-server/store/book_favourites/`

const favouritesSocket = new WebSocket(book_favourites_url)


if(document.getElementsByClassName('books').length > 0) {
    console.log('We have books element on the page!')
    var books_element = document.getElementsByClassName('books')[0]
    books_in_favourites(books_element)
}

if (document.getElementsByClassName('book-detail').length > 0) {
    console.log('We have book detail element on the page!')
    var book_detail_element = document.getElementsByClassName('book-detail')[0]
    book_detail_in_favourites(book_detail_element)
}

function add_remove_book_favourites(el) {
    var book_id = el.id

    favouritesSocket.send(JSON.stringify({
        'message_type': 'add_remove_book_favourites',
        'book_id': book_id
    }))

    el.classList.toggle('in_favourites')
    if (el.classList.contains('in_favourites')) {
        el.innerHTML = 'В избранном'
    }
    else {
        el.innerHTML = 'В избранное'
    }
}

function books_in_favourites(element) {
    if (favouritesSocket.readyState) {
        var books = element.getElementsByClassName('book')

        favouritesSocket.send(JSON.stringify({
            'message_type': 'books_in_favourites'
        }))

        favouritesSocket.onmessage = function (e) {
            var data = JSON.parse(e.data)
            var books_id_set = data['books_id_set']
            for (var i = 0; i < books.length; i++) {
                if (books_id_set.includes(parseInt(books[i].id))) {
                    var favourites_btn = books[i].getElementsByClassName('favourites')[0].getElementsByTagName('span')[0]
                    favourites_btn.classList.add('in_favourites')
                    favourites_btn.innerHTML = 'В избранном'
                }
            }
        }

    }
    else {
        setTimeout(function () {
            books_in_favourites(element)
        }, 50)
    }
}

function book_detail_in_favourites(element) {
    if (favouritesSocket.readyState) {
        favouritesSocket.send(JSON.stringify({
            'message_type': 'books_in_favourites'
        }))

        favouritesSocket.onmessage = function (e) {
            var data = JSON.parse(e.data)
            var books_id_set = data['books_id_set']
            if (books_id_set.includes(parseInt(element.id))) {
                var favourites_btn = element.getElementsByClassName('favourites')[0].getElementsByTagName('span')[0]
                favourites_btn.classList.add('in_favourites')
                favourites_btn.innerHTML = 'В избранном'
            }
        }

    }
    else {
        setTimeout(function () {
            book_detail_in_favourites(element)
        }, 50)
    }
}