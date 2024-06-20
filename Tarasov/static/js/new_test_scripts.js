window.onload = function() {
    if (window.location.hash) {
        // Удаляем хеш-часть URL
        history.replaceState(null, null, window.location.pathname + window.location.search);
    }
};

const timeInput = document.getElementById('timeInput');

timeInput.addEventListener('input', function(e) {
	// Удаляем все символы, кроме цифр
	let value = e.target.value.replace(/[^\d]/g, '');

	// Добавляем двоеточие после двух цифр
	if (value.length === 2) {
		e.target.value = value + ':';
	} else if (value.length > 2) {
	// Если введено больше двух цифр, форматируем как ЧЧ:ММ
		e.target.value = value.slice(0, 2) + ':' + value.slice(2, 4);
	}
});

// Предотвращаем ввод букв и других символов
timeInput.addEventListener('keypress', function(e) {
	if (!/\d/.test(e.key)) {
		e.preventDefault();
	}
});

function deleteAns(linkGoBack) {
	linkGoBack.parentElement.remove();

	checkNeededInputs();
}

function adjustHeight(textarea) {
 	textarea.style.height = "auto";
    textarea.style.height = textarea.scrollHeight + "px";
} 

function createAns(linkAddAns) {
	let ansContainer = linkAddAns.parentElement;

	let div = document.createElement('div');
    div.className = 'link-block';

    let label = document.createElement('label');

    let input = document.createElement('input');
    input.className = 'needed-input answer-checkbox';
    input.type = 'checkbox';
    input.name = 'correct';
    input.value = 'yes';

    let span = document.createElement('span');
    span.className = 'answer-checkmark';
    span.title = 'Отметить правильный ответ';	

    let textarea = document.createElement('textarea');
    textarea.className = 'needed-input answer-input text';
    textarea.maxLength = '64';
    textarea.placeholder = 'Введите ответ';
    textarea.spellcheck = false;

    let link = document.createElement('a');
    link.className = 'del-ans';
    link.href = '#';
    link.title = 'Убрать ответ';

    textarea.oninput = function() { onTextInput(this); };
    link.onclick = function() { deleteAns(this); };
    input.oninput = function() { checkNeededInputs(); };

    div.appendChild(label);
    div.appendChild(textarea);
    div.appendChild(link);
    label.appendChild(input);
    label.appendChild(span);

    ansContainer.appendChild(div);
}

function addQuestion() {
	let newQuestion = document.createElement('div');
	newQuestion.className = 'slide-container question';
	newQuestion.id = 'q' + (document.getElementsByClassName('question').length + 1);

    let mainContainer = document.createElement('div');
    mainContainer.className = 'main-container';

    let questionInput = document.createElement('textarea');
    questionInput.className = 'needed-input question-input title text';
    questionInput.maxLength = '256';
    questionInput.placeholder = 'Введите вопрос';
    questionInput.spellcheck = false;

    let underline = document.createElement('hr');
    underline.className = 'underline';

    let mainSubcontainer = document.createElement('div');
    mainSubcontainer.className = 'main-subcontainer';

    let leftSubcontainer = document.createElement('form');
    leftSubcontainer.className = 'info-subcontainer';

    let picLogo = document.createElement('div');
    picLogo.className = 'stud-logo-subcontainer';

    let labelUpload = document.createElement('label');
    labelUpload.htmlFor = 'file-upload';
    labelUpload.className = 'file-upload text';

    let inputUpload = document.createElement('input');
    inputUpload.id = 'file-upload';
    inputUpload.className = 'text';
    inputUpload.type = 'file';
    inputUpload.name = 'photo';
    inputUpload.accept = 'image/*';

    let verticalLine = document.createElement('hr');
    verticalLine.className = 'vertical-line';

    let answersContainer = document.createElement('div');
    answersContainer.className = 'info-subcontainer answers-container';

    let linkAddAns = document.createElement('a');
    linkAddAns.id = 'link-add-ans';
    linkAddAns.className = 'sign sign-up text';
    linkAddAns.href = '#';
    linkAddAns.textContent = 'Добавьте вариант ответа';

    let linkInDropdown = document.createElement('button');
    linkInDropdown.className = 'text dropdown-link';
    linkInDropdown.value = '#' + newQuestion.id;
    linkInDropdown.textContent = 'Вопрос ' + (document.getElementsByClassName('question').length + 1);

    questionInput.oninput = function() { onTextInput(this); };
    linkAddAns.onclick = function() { createAns(this); };
    linkInDropdown.onclick = function() { MoveToQuestion(this); };

    labelUpload.appendChild(inputUpload);
    leftSubcontainer.appendChild(picLogo);
    leftSubcontainer.appendChild(labelUpload);
    answersContainer.appendChild(linkAddAns);
    mainSubcontainer.appendChild(leftSubcontainer);
    mainSubcontainer.appendChild(verticalLine);
    mainSubcontainer.appendChild(answersContainer);
    mainContainer.appendChild(questionInput);
    mainContainer.appendChild(underline);
    mainContainer.appendChild(mainSubcontainer);
    newQuestion.appendChild(mainContainer);

    document.getElementById('slider-questions').appendChild(newQuestion);
    document.getElementById('dropdown-content').appendChild(linkInDropdown);

    checkNeededInputs();
}

function checkCorrectHrefs() {
	let dropdownLinks = document.getElementsByClassName('dropdown-link');
	let questions = document.getElementsByClassName('question');

	for (let i = 0; i < dropdownLinks.length; i++) {
		if (dropdownLinks[i].value != '#q' + (i + 1)) {
			for (let j = 0; j < questions.length; j++) {
				if (questions[j].id == dropdownLinks[i].value.substring(1)) questions[j].id = 'q' + (i + 1);
			}
			dropdownLinks[i].value = '#q' + (i + 1);
		}
	}
}

function checkCorrectNumQuestion() {
	if (document.getElementById('num-question').textContent.substring(7) > document.getElementsByClassName('dropdown-link').length) {
		document.getElementById('num-question').textContent = 'Воспрос ' + document.getElementsByClassName('dropdown-link').length;
	}
}

function delQuestion() {
	let countQuestions = document.getElementsByClassName('question').length;

	if (countQuestions > 1) {
		let currentQuestion = document.location.hash.substring(1);

		if (currentQuestion == '') currentQuestion = document.getElementsByClassName('dropdown-link')[0].value.substring(1);

		document.getElementById(currentQuestion).remove();

		let dropdownLinks = document.getElementsByClassName('dropdown-link');
		let numCurrDropdownLink;

		for (let i = 0; i < dropdownLinks.length; i++) {
			if (i > numCurrDropdownLink) dropdownLinks[i].textContent = 'Вопрос ' + i;
			if (dropdownLinks[i].value == '#' + currentQuestion) numCurrDropdownLink = i;
		}

		dropdownLinks[numCurrDropdownLink].remove();
	}

	checkCorrectHrefs();
	checkCorrectNumQuestion();

	checkNeededInputs();
}

function MoveToQuestion(dropdownLink) {
	document.getElementById('num-question').textContent = 'Вопрос ' + dropdownLink.value.substring(2);

	location.href = dropdownLink.value;
}

function goBackToQuestion() {
	let hrefCurrentQuestion = document.location.hash;
	let questionLinks = document.getElementsByClassName('dropdown-link');
	let numQuestion = document.getElementById('num-question');
	
	if (hrefCurrentQuestion == '') hrefCurrentQuestion = '#q1';

	if (hrefCurrentQuestion.substring(2) == 1) {
		numQuestion.textContent = 'Вопрос ' + questionLinks.length;

		setTimeout(() => location.href = questionLinks[questionLinks.length - 1].value, 0);
	} else {
		numQuestion.textContent = 'Вопрос ' + (Number(hrefCurrentQuestion.substring(2)) - 1);

		setTimeout(() => location.href = '#q' + (Number(hrefCurrentQuestion.substring(2)) - 1), 0);
	}
}

function goToQuestion() {
	let hrefCurrentQuestion = document.location.hash;
	let questionLinks = document.getElementsByClassName('dropdown-link');
	let numQuestion = document.getElementById('num-question');

	if (hrefCurrentQuestion == '') hrefCurrentQuestion = '#q1';

	if (hrefCurrentQuestion.substring(2) == questionLinks.length) {
		numQuestion.textContent = 'Вопрос 1';

		setTimeout(() => location.href = questionLinks[0].value, 0);
	} else {
		numQuestion.textContent = 'Вопрос ' + (Number(hrefCurrentQuestion.substring(2)) + 1);

		setTimeout(() => location.href = '#q' + (Number(hrefCurrentQuestion.substring(2)) + 1), 0);
	}
}

//console.log(document.getElementById('q1').querySelectorAll('.info-subcontainer').length);

function checkNeededInputs() {
	let questions = document.getElementsByClassName('question');
	const countQuestions = questions.length;
	let countNotEmptyInputs = 0, countNeededInputs = 0;
	let checkTakeTest = false;

	for (let i = 0; i < countQuestions; i++) {
		let checkQuestion = false, checkAns = false, checkAnsNotEmpty = true, checkTrueAns = false;
		let neededInputs = document.querySelectorAll('#' + questions[i].id + ' .needed-input');
		
		for (let j = 0; j < neededInputs.length; j++) {
			if (neededInputs[j].classList.contains('answer-check')) {
				if (neededInputs[j].checked == true) checkTrueAns = true;
				checkTakeTest = true;
			}
			if (neededInputs[j].classList.contains('answer-checkbox') && neededInputs[j].checked == true) checkTrueAns = true;
			if (neededInputs[j].classList.contains('question-input') && neededInputs[j].value != '') checkQuestion = true;
			if (neededInputs[j].classList.contains('answer-input') && checkAnsNotEmpty) {
				if (neededInputs[j].value != '') checkAns = true; else {
					checkAns = false;
					checkAnsNotEmpty = false;
				}
			}
		}

		if (checkQuestion) countNotEmptyInputs++;
		if (checkAns) countNotEmptyInputs++;
		if (checkTrueAns) countNotEmptyInputs++;

		if (checkTakeTest) countNeededInputs = countNeededInputs + 1; else countNeededInputs = countNeededInputs + 3;
	}

	if (!checkTakeTest) {
		if (timeInput.value != '') countNotEmptyInputs++;
		countNeededInputs++;
	}

	let percentage = countNotEmptyInputs / countNeededInputs * 100;

	progress.style.backgroundSize = percentage + '%';
	
	if (percentage == 100) {
		progress.type = 'submit';
		progress.textContent = 'Завершить';
	} else {
		progress.type = 'button';
		progress.textContent = Math.round(percentage) + '%';
	}
}

function onTextInput(textElem) {
	checkNeededInputs();
	adjustHeight(textElem);
}

let countdown = setInterval(function() {
	let minutes = Number(timeInput.textContent.substring(0, 2));
	let seconds = Number(timeInput.textContent.substring(3, 5));
	let time = minutes * 60 + seconds;

	time--;

	minutes = Math.floor(time / 60);
	seconds = time % 60;

	timeInput.innerHTML = (minutes < 10 ? "0" + minutes : minutes) + ":" + (seconds < 10 ? "0" + seconds : seconds);

	if (time <= 0) {
		clearInterval(countdown);
		console.log("Время истекло!");
	}
}, 1000);