addEventInputs();

function addEventInputs() {
	let inputs = document.getElementsByTagName('input');

	for (let i = 0; i < inputs.length; i++) {
		inputs[i].addEventListener('input', () => {
			inputClass = inputs[i].classList[0];
			addEventFinalLinks(isEndSignUp(inputClass), inputClass);
		});
	}
}

function isEndSignUp(classNameForm) {
	let formInputs = document.getElementsByClassName(classNameForm);

	let flagEmptyInput = false;
	let flagCheckedInput = false;
	let flagMissCheckboxes = true;

	for (let i = 0; i < formInputs.length; i++) {
		if (formInputs[i].type == 'radio') {
			flagMissCheckboxes = false;

			if (formInputs[i].checked) {
				flagCheckedInput = true;
			}
		} else {
			if (formInputs[i].value == '') {
				flagEmptyInput = true;
			}
		}
	}

	return flagMissCheckboxes == true ? !flagEmptyInput : !flagEmptyInput && flagCheckedInput;
}

function addEventFinalLinks(flagEndSignUp, partTitleClass) {
	let titleEndSignUp = document.querySelector('.title-' + partTitleClass);

	if (flagEndSignUp) {
		titleEndSignUp.style.color = '#264A33';
		titleEndSignUp.type = 'submit';
		titleEndSignUp.classList.add('breathing-sign');
	} else {
		titleEndSignUp.style.color = '#0D121A';
		titleEndSignUp.type = 'button';
		titleEndSignUp.classList.remove('breathing-sign');
	}
}