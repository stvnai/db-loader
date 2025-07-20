

const customSelect = document.querySelector('.custom-select');
const selectHeader = document.querySelector('.select-header');

// DROPDOWN FUNCTION

function toggle_dropdown(event) 

{ 
    customSelect.classList.toggle("open")
};

// SELECT FUNCTION

function select_option(event) 

{
    const selectedOption = event.target;
    const index = selectedOption.getAttribute("data-index");
    const label = selectedOption.textContent;
    
    customSelect.classList.remove("open");
    
    customSelect.setAttribute("selected-index", index);
    selectHeader.textContent = label;
    
    document.getElementById("selected-athlete-input").value = index;

};



function click_outside(event) {
    
    if (!customSelect.contains(event.target) && customSelect.classList.contains("open")) 
        {
            customSelect.classList.remove("open");
        }
    };
    
    
    
    
    
    
const options = document.querySelectorAll(".option");

// APPLYING FUNCTIONS

selectHeader.addEventListener("click", toggle_dropdown);

document.addEventListener("click", click_outside);

options.forEach(option => {option.addEventListener("click", select_option);

});


