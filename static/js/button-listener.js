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
    for (let id in buttonStates) {
        if (buttonStates[id]) {
            if (id === "button1") {


                let contentContainer = document.getElementById("content-section2");
                let loadingElement = document.getElementById("loading");


                contentContainer.style.display = "block";
                loadingElement.style.display = "block";

                fetch(`/top-artists?num_artists=15`)
                .then(response => response.json())
                .then(data => {

                    let content = '<div>';
                    data.forEach(entry => {
                        let artist = entry[0], duration = entry[1], count = entry[2], imageURL = entry[3];
                        content += `
                            <button class="artistButton" onclick="buttonClicked(this)">
                                <div class="buttonInfo">
                                    <div class="imageContainer">
                                        <img src="${imageURL}" alt="Artist Image" class="artistImage">
                                    </div>
                                    <div class="textContainer">
                                        <div class="mainName">${artist}</div> 
                                        <div class="minutesListened">${count} streams • ${duration} streamed</div>
                                    </div>
                                </div>
                            </button>`;
                    })
                    content += '</div>';


                    contentContainer.innerHTML = content;
                    loadingElement.style.display = 'none';
                })
                .catch((error) => {
                   console.error('Error:', error);
                   loadingElement.style.display = "none";
                });
            } else {

            }
        } else if (id === "button1") {

            document.getElementById("content-section2").style.display = "none";
        }
    }
}

function buttonClicked(button) {
    const buttons = document.getElementsByClassName("artistButton");

    for (let i = 0; i < buttons.length; i++) {
        buttons[i].classList.remove('clicked');
    }
    button.classList.toggle('clicked')
}

updateResetButtonVisibility();