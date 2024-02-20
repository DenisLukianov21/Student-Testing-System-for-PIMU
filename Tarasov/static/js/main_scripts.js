function viewTopSubArea(valueChooseElem, classElem) {
    changeColorElem(valueChooseElem, classElem);

    let subTopArea = document.getElementById('sub-top');
    subTopArea.style.background = 'rgb(255, 75, 73, 1.0)';
    subTopArea.style.display = 'block';   
}

function viewBottomSubArea(valueChooseElem, classElem) {
    changeColorElem(valueChooseElem, classElem);

    let subBottomArea = document.getElementById('sub-bottom');
    subBottomArea.style.background = 'rgb(255, 75, 73, 1.0)';
    subBottomArea.style.display = 'block';

    if (document.getElementById('courses').style.display === 'none') {
        document.getElementById('help-video').style.display = 'block';
    }   
}

function changeColorElem(textCurrElem, classElem) {
    let allElem = document.querySelectorAll(classElem);

    for(let elem of allElem) {
        if (textCurrElem == elem.textContent) {
            elem.style.color = 'rgb(211, 81, 80, 1.0)';
        } else {
            elem.style.color = '#FF9966';
        }
    }

    document.getElementById('main').style.background = 'rgb(235, 235, 235, 1.0)';
    document.getElementById('sub-top').style.background = 'rgb(235, 235, 235, 1.0)';
    document.getElementById('sub-bottom').style.background = 'rgb(235, 235, 235, 1.0)';
    document.getElementById('exit').style.background = '#66CCCC';
    document.getElementById('exit').style.color = 'white';
}

function viewMyCourses(valueChooseElem, classElem) {
    viewTopSubArea(valueChooseElem, classElem);

    let courses = document.querySelectorAll('.courses');

    for(let course of courses) {
        course.style.color = 'white';
    }
    document.getElementById('courses').style.display = 'flex';
    document.getElementById('userID').style.display = 'none';
    document.getElementById('statistics').style.display = 'none';
    document.getElementById('questions').style.display = 'none';
    document.getElementById('help-video').style.display = 'none';
}

function viewMyPage(valueChooseElem, classElem) {
    viewBottomSubArea(valueChooseElem, classElem);

    for(let test of document.querySelectorAll('.tests')) {
        test.style.display = 'none';
    }

    document.getElementById('courses').style.display = 'none';
    document.getElementById('userID').style.display = 'block';
    document.getElementById('statistics').style.display = 'flex';
    document.getElementById('questions').style.display = 'none';
    document.getElementById('help-video').style.display = 'none';
}

function viewInfo(valueChooseElem, classElem) {
    viewTopSubArea(valueChooseElem, classElem);
    
    let questions = document.querySelectorAll('.questions');

    for(let question of questions) {
        question.style.color = 'white';
    }

    for(let test of document.querySelectorAll('.tests')) {
        test.style.display = 'none';
    }

    document.getElementById('courses').style.display = 'none';
    document.getElementById('userID').style.display = 'none';
    document.getElementById('statistics').style.display = 'none';
    document.getElementById('questions').style.display = 'flex';
}

function viewTests(valueChooseElem, slug, classElem) {
    viewBottomSubArea(valueChooseElem, classElem);

    let subBottomArea = document.getElementById('sub-bottom');
    subBottomArea.style.background = 'rgb(255, 75, 73, 1.0)';
    subBottomArea.style.display = 'block';
    
    let tests = document.querySelectorAll('.tests');

    for(let test of tests) {
        if (test === document.getElementById(slug)) {
            test.style.display = 'flex';
        } else {
            test.style.display = 'none';
        }
    }
}