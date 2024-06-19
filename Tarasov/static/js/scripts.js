var slideIndex = 1;
	
showSlides(slideIndex);

function showSlides(currentSlide) {
	let slides = document.getElementsByClassName('dot-slide');
	
	for (let i = 0; i <= 2; i++) {
		if (i == currentSlide) {
			slides[i].style.background = 'white';

			if (currentSlide == 0) document.getElementById(slides[i].attributes.href.value.slice(1)).style.display = 'flex';

			setTimeout(() => location.href = slides[i].href, 0);
		} else {
			slides[i].style.background = '#A38C7A';
		}
	}
}

function highlightLink(partSelector) {
	let pass = document.querySelector('.pass-' + partSelector);
	let login = document.querySelector('.login-' + partSelector);

	if (pass.value !== '' && login.value !== '') {
		document.querySelector('.title-' + partSelector).style.color = '#264A33';
		document.querySelector('.title-' + partSelector).classList.add('breathing-sign');
        document.querySelector('.title-' + partSelector).type = 'submit';
	} else {
		document.querySelector('.title-' + partSelector).style.color = '#0D121A';
		document.querySelector('.title-' + partSelector).classList.remove('breathing-sign');
        document.querySelector('.title-' + partSelector).type = 'button';
	}
}