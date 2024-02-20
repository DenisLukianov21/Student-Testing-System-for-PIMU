function checkCheckbox() {
    const checkboxes = document.querySelectorAll('.answer');
    let flag = false; 

    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            flag = true;
        }
    }

    if (flag) {
        viewSubmit();
    } else {
        document.getElementById('next-page').style.display = 'flex';
        document.getElementById('submit-form').style.display = 'none';
        document.getElementById('question-area').style.background = 'rgb(255, 75, 73, 1.0)';
        document.getElementById('question').style.color = 'white';
    }
}

function checkRadiobox() {
    const checkboxes = document.querySelectorAll('.answer');
    let flag = false; 

    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            flag = true;
        }
    }

    if (flag) {
        viewSubmit();
    }
}

function viewSubmit() {
    document.getElementById('next-page').style.display = 'none';
    document.getElementById('submit-form').style.display = 'flex';
    document.getElementById('question-area').style.background = 'rgb(235, 235, 235, 1.0)';
    document.getElementById('question').style.color = 'black';
}

function showAndTimeoutResult() {
    const result = document.getElementById('result');

    result.style.display = 'flex';
    document.getElementById('submit-form').style.display = 'none';

    setTimeout( () => {
        result.style.display = 'none';
        document.getElementById('next-page').style.display = 'flex';
    }, 2500);
}