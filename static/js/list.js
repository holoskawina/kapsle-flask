

if (localStorage.getItem('expandElements') === null) {
    localStorage.setItem('expandElements', '[]')
}

let i = 0
document.querySelectorAll('li>a:not(:only-child)').forEach(element => {
    const icon = document.createElement('i')
    const id = `listitem${i}`
    element.id = id
    element.appendChild(icon)
    let expandElements = JSON.parse(localStorage.getItem('expandElements'))
    if (expandElements.includes(id)) {
        element.classList.add('list-minus')
        icon.className = 'fas fa-minus'
    }
    else {
        expandElements.push(id)
        element.classList.add('list-plus')
        icon.className = 'fas fa-plus'
    }
    icon.onclick = function () { toggle_list(this); return false }
    i++
});
if (localStorage.getItem('hideCouintriesList') === 'true') {
    localStorage.setItem('hideCouintriesList', "false")
} else {
    localStorage.setItem('hideCouintriesList', "true")
}
toggleCountriesList()

const list = document.getElementById('countries-list')
list.onscroll = () => { localStorage.setItem('scrollPos', list.scrollTop) }
list.scrollTop = localStorage.getItem('scrollPos')

function toggle_list(element) {
    let expandElements = JSON.parse(localStorage.getItem('expandElements'))
    const id = element.parentElement.id
    if (expandElements.includes(id)) {
        expandElements = expandElements.filter(e => e !== id)
        element.parentElement.classList.add('list-plus')
        element.parentElement.classList.remove('list-minus')
        element.classList.add('fa-plus')
        element.classList.remove('fa-minus')
    }
    else {
        expandElements.push(id)
        element.parentElement.classList.remove('list-plus')
        element.parentElement.classList.add('list-minus')
        element.classList.remove('fa-plus')
        element.classList.add('fa-minus')
    }
    localStorage.setItem('expandElements', JSON.stringify(expandElements))
}

function changePage(offset) {
    let href = window.location.href;
    if (href.includes('offset=')) {
        window.location.href = href.replace(/offset=\d*/, 'offset=' + offset)
    }
    else {
        if (href.includes('?')) {
            window.location.href += '&offset=' + offset
        } else {
            window.location.href += '?offset=' + offset
        }
    }
}
function nextPage(page = 1) {
    let href = window.location.href;
    let offset = 0
    let limit = 500
    if (/offset=\d*/.exec(href) !== null) {
        offset = /offset=\d*/.exec(href)[0].replace('offset=', '')
    }
    if (/limit=\d*/.exec(href) !== null) {
        limit = /limit=\d*/.exec(href)[0].replace('limit=', '')
    }
    changePage(page * limit + offset * 1)
}
function changeLimit(limit) {
    if (limit > 500) {
        limit = 500
    }
    let href = window.location.href;
    if (href.includes('limit=')) {
        window.location.href = href.replace(/limit=\d*/, 'limit=' + limit)
    }
    else {
        if (href.includes('?')) {
            window.location.href += '&limit=' + limit
        } else {
            window.location.href += '?limit=' + limit
        }
    }
}
function toggleCountriesList() {
    const list = document.getElementById('countries-list')
    const button = document.getElementById('countries-list-toggle')
    if (localStorage.getItem('hideCouintriesList') === 'true') {
        localStorage.setItem('hideCouintriesList', "false")
        list.style.display = 'block'
        button.innerHTML = '<i class="fas fa-angle-left"></i>'
        button.style.left = '280px'
        document.getElementById('content').style.marginLeft = '280px'
        document.getElementById('menu').style.marginLeft = '280px'
    } else {
        localStorage.setItem('hideCouintriesList', "true")
        list.style.display = 'none'
        button.innerHTML = '<i class="fas fa-angle-right"></i>'
        button.style.left = '0px'
        document.getElementById('content').style.marginLeft = '0px'
        document.getElementById('menu').style.marginLeft = '0px'
    }
}