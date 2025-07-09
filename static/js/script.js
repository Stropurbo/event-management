document.addEventListener('DOMContentLoaded', function () {
	const catdropdown = document.getElementById('categoryDropdown')
	const catlist = document.getElementById('categoryList')

	catdropdown.addEventListener('click', function () {
		catlist.classList.toggle('hidden')
	})

	document.querySelectorAll('.catItem').forEach((item) => {
		item.addEventListener('click', function () {
			selectItem.textContent = this.textContent
			catlist.classList.add('hidden')
		})
	})

	document.addEventListener('click', function (event) {
		if (!catdropdown.contains(event.target)) {
			catlist.classList.add('hidden')
		}
	})
})

document.getElementById('menu-toggle').addEventListener('click', function () {
	document.getElementById('menu').classList.toggle('hidden')
})

setTimeout(function () {
	var alert = document.querySelector('.alert-container')
	if (alert) {
		alert.style.display = 'none'
	}
}, 2000)

// ata user icon a click korle logout r dashboard show hobe
document.getElementById('menu-toggle').addEventListener('click', function () {
	document.getElementById('mobile-menu').classList.toggle('hidden')
})

// document.getElementById('user-menu-button').addEventListener('click', function () {
// 	document.getElementById('user-menu').classList.toggle('hidden')
// })

document.addEventListener('DOMContentLoaded', function () {
	const button = document.getElementById('user-menu-button')
	const menu = document.getElementById('user-menu')

	if (button && menu) {
		button.addEventListener('click', function () {
			menu.classList.toggle('hidden')
		})
	} else {
		console.warn('user-menu-button or user-menu not found in the DOM.')
	}
})
  

window.addEventListener('click', function (e) {
	if (!document.getElementById('user-menu-button').contains(e.target)) {
		document.getElementById('user-menu').classList.add('hidden')
	}
})

// ata category er jonno
document.getElementById('category-text').addEventListener('click', function () {
	document.getElementById('cat-list').classList.toggle('hidden')
})

window.addEventListener('click', function (e) {
	if (!document.getElementById('category-text').contains(e.target)) {
		document.getElementById('cat-list').classList.add('hidden')
	}
})

// speaker 





  


/////////////

