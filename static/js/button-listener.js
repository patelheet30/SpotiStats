let buttons = document.getElementsByClassName("button");
let resetButton = document.getElementById("reset");

let buttonStates = {
    "button1": false,
    "button2": false,
}

function updateResetButtonVisibility() {
    let button1 = document.getElementById('button1');
    let button2 = document.getElementById('button2');

    if (buttonStates["button1"]) {
        button2.style.display = "none";
        resetButton.style.display = "inline-block";
    }

    else if (buttonStates["button2"]) {
        button1.style.display = "none";
        resetButton.style.display = "inline-block";
    }

    else {
        button1.style.display = "inline-block";
        button2.style.display = "inline-block";
        resetButton.style.display = "none";
    }
}

Array.from(buttons).forEach(button => {
    button.addEventListener("click", function() {
        let id = this.getAttribute('id');
        if (this.classList.contains('reset')) {
            for (let key in buttonStates) {
                buttonStates[key] = false;

                let currentButton = document.getElementById(key);
                if(currentButton){
                    currentButton.style.backgroundColor = "";
                    currentButton.style.color = "";
                    currentButton.style.display = "inline-block";
                }
            }
            updateContentSection();
            this.style.display = "none";
        } else {

            let wasSelected = buttonStates[id];

            for (let key in buttonStates) {
                buttonStates[key] = false;
                let currentButton = document.getElementById(key);
                if(currentButton){
                    currentButton.style.backgroundColor = "";
                    currentButton.style.color = "";
                }
            }


            buttonStates[id] = !wasSelected;
            if (buttonStates[id]) {
                this.style.backgroundColor = "#FFFFFFFF";
                this.style.color = "#232323FF";
            }

            updateResetButtonVisibility();
            updateContentSection();
        }
    });
});

function updateContentSection() {
    let contentContainer = document.getElementById("content-section2");
    let loadingElement = document.getElementById("loading");

    if (contentContainer) {
        contentContainer.innerHTML = '';
        contentContainer.style.display = "none";
    }

    let isAnyButtonSelected = false;

    for (let id in buttonStates) {
        if (buttonStates[id]) {
            isAnyButtonSelected = true;
            if(contentContainer) {
                contentContainer.style.display = "block";
            }

            const content_type = id === "button1" ? "artists" : "albums";
            fetch('/get_content', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                  content_type: content_type,
                  num_items: '15',
                }),
            })
            .then(response => response.text())
            .then(data => {
                if(contentContainer) {
                    contentContainer.innerHTML = data;
                }
                if(loadingElement) {
                    loadingElement.style.display = "none";
                }
            })
            .catch((error) => {
               console.error('Error:', error);

               if (loadingElement) {
                   loadingElement.style.display = "none";
               }
            });
        }
    }

    if (loadingElement) {
        if (isAnyButtonSelected) {
            loadingElement.style.display = "block";
        } else {
            loadingElement.style.display = "none";
        }
    }

}

function buttonClicked(button) {
    const buttons = document.getElementsByClassName("artistButton");

    for (let i = 0; i < buttons.length; i++) {
        buttons[i].classList.remove('clicked');
    }
    button.classList.toggle('clicked')

    const info = JSON.parse(button.getAttribute('data-info'));

    // Ajax call to Flask server
    fetch('/get_the_info', {
        method:'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            click_info:info
        })
    })
    .then(response => response.text())
    .then(data => {
        const rightContainer = document.getElementsByClassName("right-container")[0];
        if(rightContainer) {
            rightContainer.innerHTML = data;
        }
    });
}

updateResetButtonVisibility();