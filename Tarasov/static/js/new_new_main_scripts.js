var checkStatGroups = false, checkStatCourses = false, checkStatTests = false;

addEventChoiceStatElems();
addEventRadioboxes();

var courses = document.getElementsByClassName('course');
var questions = document.getElementsByClassName('question');

addEventElemPage(courses);

addEventDeleteElems();

addEventListGroupsLinks();

slideIndex = 2;
addEventElemPage(questions);

function addEventChoiceStatElems() {
	let choiceStatElems = document.getElementsByClassName('choice-stat-elem');

	for (let i = 0; i < choiceStatElems.length; i++) {
		choiceStatElems[i].addEventListener('click', () => {
			switch (i) {
				case 0:
				case 1:
					setTimeout(() => choiceStatElems[i].href = '#stat-list-groups', 0);
					showTitleChooseElem('title-stat-groups');
					break;
				case 2:
				case 3:
					setTimeout(() => choiceStatElems[i].href = '#stat-list-courses', 0);
					showTitleChooseElem('title-stat-courses');
					break;
				case 4:
				default:
					setTimeout(() => choiceStatElems[i].href = '#stat-list-tests', 0);
					showTitleChooseElem('title-stat-tests');
					break;
			}
		});
	}
}

function addEventClosePageLinks() {
	let closePageLinks = document.getElementsByClassName('stat-return');

	for (let i = 0; i < closePageLinks.length; i++) {
		closePageLinks[i].addEventListener('click', () => {
			if (checkStatGroups && checkStatCourses && checkStatTests) {
				setTimeout(() => location.href = '#stat-result-page', 0);
				showTitleChooseElem('title-stat-result');

				changeColorStatResult();
			} else {
				setTimeout(() => location.href = '#empty-stat-page', 0);
				showTitleChooseElem('title-stat-start');
			}
		});
	}
}

function addEventRadioboxes() {
	let radioboxes = document.querySelectorAll('input.stat-groups, input.stat-courses, input.stat-tests');
	

	let blocksStatElem = document.getElementsByClassName('link-block-stat');

	for (let i = 0; i < radioboxes.length; i++) {
		let nameRadiobox = radioboxes[i].parentElement.children[1].textContent;

		if (radioboxes[i].classList.contains('stat-groups')) {
			radioboxes[i].addEventListener('click', () => {
				checkStatGroups = true;
				showChooseNameStatElem(nameRadiobox, blocksStatElem[0]);
				addEventClosePageLinks();
			});
		} else if (radioboxes[i].classList.contains('stat-courses')) {
			radioboxes[i].addEventListener('click', () => {
				checkStatCourses = true;
				showChooseNameStatElem(nameRadiobox, blocksStatElem[1]);
				addEventClosePageLinks();
				showTestsChoosedCourse(radioboxes[i]);
			});
		} else if (radioboxes[i].classList.contains('stat-tests')) {
			radioboxes[i].addEventListener('click', () => {
				checkStatTests = true;
				showChooseNameStatElem(nameRadiobox, blocksStatElem[2]);
				addEventClosePageLinks();
			});
		}
	}
}

function showTestsChoosedCourse(course) {
	let tests = document.querySelectorAll('input.stat-tests');

	for (let i = 0; i < tests.length; i++) {
		if (tests[i].classList.contains(course.id + '-stat-tests')) tests[i].parentElement.style.display = 'flex';
		else tests[i].parentElement.style.display = 'none';
	}
}

function showChooseNameStatElem(nameChooseRadiobox, blockStatElem) {
	let statElem = blockStatElem.children[0], hiddenStatElem = blockStatElem.children[1];

	if (hiddenStatElem.offsetParent === null) {
		hiddenStatElem.innerText = nameChooseRadiobox;
		pseudoslideElems(statElem, hiddenStatElem);		
	} else {
		statElem.classList.remove('no-change');
		statElem.classList.add('have-change');
		statElem.innerText = nameChooseRadiobox;
		pseudoslideElems(hiddenStatElem, statElem);
	}
}

function changeColorStatResult() {
	const startValue = 50, endValue = 100;
	const startRed = 110, endRed = 38;
	const startGreen = 59, endGreen = 74;
	const startBlue = 48, endBlue = 51;

	let valuesStatResult = document.querySelectorAll('font.text-stat-result');

	for (let i = 0; i < valuesStatResult.length; i++) {
		const value = valuesStatResult[i].textContent;

		const red = getColorForValue(startValue, endValue, value, startRed, endRed);
		const green = getColorForValue(startValue, endValue, value, startGreen, endGreen);
		const blue = getColorForValue(startValue, endValue, value, startBlue, endBlue);

		valuesStatResult[i].style.color = 'rgb(' + red + ', ' + green + ', ' + blue + ', 1.0)';
		valuesStatResult[i].parentElement.style.color = 'rgb(' + red + ', ' + green + ', ' + blue + ', 1.0)';
	}	
}

function getColorForValue(startValue, endValue, value, startColor, endColor) {
	return startColor + (endColor - startColor) * (value - startValue) / (endValue - startValue);
}

function addEventDeleteElems() {
	let deleteElems = document.querySelectorAll('.remove-elem');

	for (let i = 0; i < deleteElems.length; i++) {
		let mainBlockElem = deleteElems[i].parentElement;
		let deleteBlockElem = mainBlockElem.parentElement.children[1];

		deleteElems[i].addEventListener('click', () => {
			pseudoslideElems(mainBlockElem, deleteBlockElem);

			if (deleteElems[i].classList.contains('remove-course')) {
				setTimeout(() => location.href = '#help-delete-course', 0);
			} else {
				setTimeout(() => location.href = '#help-delete-test', 0);
			}
		});

		let cancelDelElem = deleteBlockElem.children[1];

		cancelDelElem.addEventListener('click', () => {
			pseudoslideElems(deleteBlockElem, mainBlockElem);

			if (cancelDelElem.classList.contains('remove-course')) {
				setTimeout(() => location.href = '#help-title-courses', 0);
			} else {
				setTimeout(() => location.href = '#help-title-tests', 0);
			}
		});
	}
}

function pseudoslideElems(fstElem, sndElem) {
	fstElem.classList.remove('show-link-list-groups');
	fstElem.classList.add('hide-link-list-groups');
	
	setTimeout(()=> {
		fstElem.style.display = 'none';

		sndElem.classList.remove('hide-link-list-groups');
		sndElem.classList.add('show-link-list-groups');

		if (sndElem.classList.contains('main-link-block') || sndElem.classList.contains('delete-link-block')) {
			sndElem.style.display = 'flex';
		} else {
			sndElem.style.display = 'block';
		}
	}, 300);
}

function addEventListGroupsLinks() {
	let openListGroups = document.querySelectorAll('.open-list-groups');
	let closeListGroups = document.querySelectorAll('.close-list-groups');
	
	for (let i = 0; i < openListGroups.length; i++) {
		openListGroups[i].addEventListener('click', () => {
			showListGroups();
			showTitleChooseElem('help-title-groups');
			pseudoslideElems(openListGroups[i], closeListGroups[i]);
		});

		closeListGroups[i].addEventListener('click', () => {
			setTimeout(() => location.href = '#courses', 0);

			if (closeListGroups[i].parentElement.id != 'form-edit-course') {
				showTitleChooseElem('title-add-course');
			} else {
				showTitleChooseElem('title-edit-course');
			}
			
			pseudoslideElems(closeListGroups[i], openListGroups[i]);		
		});
	}
	
}

function addEventElemPage(elemPage) {
	if (elemPage) {
		for (let i = 0; i < elemPage.length; i++) {
			let flagOnMyCoursesPage;

			if (flagOnMyCoursesPage = slideIndex == 1) {
				elemPage[i].addEventListener('click', () => showListTests(elemPage[i].id));

				if (elemPage[i].classList.contains('link-form-add-course')) {
					elemPage[i].addEventListener('click', showFormAddCourse);
					elemPage[i].addEventListener('click', () => showTitleChooseElem('title-add-course'));
				} else if (elemPage[i].classList.contains('link-form-edit-course')) {
					elemPage[i].addEventListener('click', () => showFormEditCourse(elemPage[i + 1]));
					elemPage[i].addEventListener('click', () => showTitleChooseElem('title-edit-course'));
				} else {
					elemPage[i].addEventListener('click', () => showTitleChooseElem('help-title-tests'));
				}
			} else if (slideIndex == 2) {
				elemPage[i].addEventListener('click', () => showListQuestions(i + 1));
				elemPage[i].addEventListener('click', () => showTitleChooseElem('help-title-videos'));
			}

			elemPage[i].addEventListener('click', () => highlightActiveLink(flagOnMyCoursesPage));
			//elemPage[i].addEventListener('click', () => addAndRemoveEventListElem(flagOnMyCoursesPage), { once: true });
		}
	}
}

function showListGroups() {
	setTimeout(() => location.href = '#list-groups', 0);
}

function showFormAddCourse() {
	setTimeout(() => location.href = '#form-add-course', 0);
}

function showFormEditCourse(editedCourse) {
	inputCourse = document.getElementById('input-edit-course');
	inputSlug = document.getElementById('input-edit-slug');

	inputCourse.value = editedCourse.textContent;
	inputSlug.value = editedCourse.id;

	setTimeout(() => location.href = '#form-edit-course', 0);
}

function showListTests(idCourse) {
	setTimeout(() => location.href = '#' + idCourse + '-tests', 0);
}

function showListQuestions(numQuestions) {
	setTimeout(() => location.href = '#question-' + numQuestions, 0);
}

function showTitleChooseElem(chooseElem) {
	setTimeout(() => location.href = '#' + chooseElem, 600);
}

function highlightActiveLink(isCoursesPage) {
	let elemPage;

	if (isCoursesPage) {
		elemPage = courses;
	} else {
		elemPage = questions;
	}

	for (let i = 0; i < elemPage.length; i++) {
		if (elemPage[i] === document.activeElement) {
			//courses[i].removeEventListener('mouseover', showTitleChooseCourses);
			//courses[i].removeEventListener('mousemove', showTitleChooseCourses);

			elemPage[i].classList.remove('sign', 'sign-up');

			elemPage[i].style.color = '#264A33';
		} else {
			//courses[i].addEventListener('mouseover', showTitleChooseCourses);
			//courses[i].addEventListener('mousemove', showTitleChooseCourses);
			if (!elemPage[i].classList.contains('edit-elem', 'remove-elem')) {
				elemPage[i].classList.add('sign', 'sign-up');

				elemPage[i].style.color = 'white';
			}
		}
	}
}

/*function addAndRemoveEventListElem(isCoursesPage) {
	let leftListElem, rightListElem, leftTitleName, rightTitleName;

	if (isCoursesPage) {
		leftListElem = document.querySelector('.list-courses');
		rightListElem = document.querySelector('.tests');
		leftTitleName = 'courses';
		rightTitleName = 'tests';
	} else {
		leftListElem = document.querySelector('.list-questions');
		rightListElem = document.querySelector('.videos');
		leftTitleName = 'questions';
		rightTitleName = 'videos';
	}

	leftListElem.removeEventListener('mouseout', () => showTitleChooseElem(leftTitleName));
	rightListElem.removeEventListener('mouseout', () => showTitleChooseElem(rightTitleName));

	rightListElem.addEventListener('mouseover', () => {
		rightListElem.addEventListener('mouseout', () => showTitleChooseElem(rightTitleName));
	});
	rightListElem.addEventListener('mouseover', () => {
		leftListElem.addEventListener('mouseout', () => showTitleChooseElem(leftTitleName));
	}, { once: true });
}*/

/*if (courses) {
	for (let i = 0; i < courses.length; i++) {
		courses[i].addEventListener('click', () => showListTests(i + 1));
		courses[i].addEventListener('click', showTitleChooseTests);
		courses[i].addEventListener('click', highlightActiveLink);
		courses[i].addEventListener('click', addAndRemoveEventListCourses, { once: true });
	}
}

function showTitleChooseTests() {
	setTimeout(() => location.href = '#help-title-tests', 350);
}

function showListTests(numCourse) {
	setTimeout(() => location.href = '#tests-' + numCourse, 0);
}

function showTitleChooseCourses() {
	setTimeout(() => location.href = '#help-title-courses', 350);
}

function highlightActiveLink() {
	for (let i = 0; i < courses.length; i++) {
		if (courses[i] === document.activeElement) {
			//courses[i].removeEventListener('mouseover', showTitleChooseCourses);
			//courses[i].removeEventListener('mousemove', showTitleChooseCourses);

			courses[i].classList.remove('sign', 'sign-up');

			courses[i].style.color = '#264A33';
		} else {
			//courses[i].addEventListener('mouseover', showTitleChooseCourses);
			//courses[i].addEventListener('mousemove', showTitleChooseCourses);

			courses[i].classList.add('sign', 'sign-up');

			courses[i].style.color = 'white';
		}
	}
}

function addAndRemoveEventListCourses() {
	let listCourses = document.querySelector('.list-courses');
	let blockTests = document.querySelector('.tests');

	listCourses.removeEventListener('mouseout', showTitleChooseCourses);
	blockTests.removeEventListener('mouseout', showTitleChooseTests);

	blockTests.addEventListener('mouseover', () => {
		blockTests.addEventListener('mouseout', showTitleChooseTests);
	});
	blockTests.addEventListener('mouseover', () => {
		listCourses.addEventListener('mouseout', showTitleChooseCourses);
	}, { once: true });
}*/