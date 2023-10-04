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
    let content = '<br/>';
    for (let id in buttonStates) {
        if (buttonStates[id]) {
            if (id === "button1") { // Assuming the button with this id corresponds to 'Artists'.
                fetch(`/top-artists?num_artists=50`)
                .then(response => response.json())
                .then(data => {
                    // Clear the content on new fetch
                    content = '<br/>';
                    data.forEach(entry => {
                        let artist = entry[0], duration = entry[1]
                        content += `${artist} (${duration} total listen duration)<br/>`;
                    })
                    // Replace the contents of "content-section2"
                    document.getElementById("content-section2").innerHTML = content;
                })
                .catch((error) => {
                   console.error('Error:', error);
                });
            } else {
               content += contents[id] + '<br/>';
            }
        }
    }
}

updateResetButtonVisibility();