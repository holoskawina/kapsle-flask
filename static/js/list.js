document.querySelectorAll('li>a:not(:only-child)').forEach(element => {
    const icon = document.createElement('i')
    icon.className = 'fas fa-plus'
    icon.onclick = function () { toggle_list(this); return false }
    element.appendChild(icon)
    element.className = 'list-plus'
});

if (localStorage.getItem('hideCouintriesList') === 'true') {
    localStorage.setItem('hideCouintriesList', "false")
} else {
    localStorage.setItem('hideCouintriesList', "true")
}
toggleCountriesList()

function toggle_list(element) {
    // element.parentElement.parentElement.lastChild.style.display='block'
    element.parentElement.classList.toggle('list-plus')
    element.parentElement.classList.toggle('list-minus')
    element.classList.toggle('fa-plus')
    element.classList.toggle('fa-minus')
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