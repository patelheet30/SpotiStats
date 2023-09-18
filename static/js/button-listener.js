let buttons = document.getElementsByClassName("button");
let resetButton = document.getElementById("reset");

let buttonStates = {
    "button1": false,
    "button2": false,
    "button3": false
}

const contents = {
    "button1": "You clicked on Artists.",
    "button2": "You clicked on Albums.",
    "button3": "You clicked on Genres."
}

function updateResetButtonVisibility() {
    let buttonSelected = Object.values(buttonStates).includes(true);
    if(buttonSelected) {
        resetButton.style.display = "inline-block";
    } else {
        resetButton.style.display = "none";
    }
}

Array.from(buttons).forEach(button => {
    button.addEventListener("click", function() {
        if(this.classList.contains('reset')) {
            for(let id in buttonStates) {
                buttonStates[id] = false;
                document.getElementById(id).style.backgroundColor = "";
                document.getElementById(id).style.color = "";
            }
            updateContentSection();

            this.style.display= "none";
        } else {
            let id = this.getAttribute('id');
            buttonStates[id] = !buttonStates[id];
            if(buttonStates[id]) {
                this.style.backgroundColor = "#FFFFFFFF";
                this.style.color = "#232323FF";
            } else {
                this.style.backgroundColor = "";
                this.style.color = "";
            }
	        updateResetButtonVisibility();
            updateContentSection();
        }
    });
});

function updateContentSection() {
    let content = '';
    for (let id in buttonStates) {
        if (buttonStates[id]) {
            content += contents[id] + '<br/>'
        }
    }
    document.getElementById("content-section2").innerHTML = content;
}

updateResetButtonVisibility();