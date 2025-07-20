


// FOR SELECT GENDER

const customGenderSelect = document.querySelector('.custom-gender-select');
const selectGenderHeader = document.querySelector('.select-gender-header');


function toggle_dropdown_gender(event) 

{ 
    customGenderSelect.classList.toggle("open")
};


function select_gender_option(event) 

{
    const selectedGenderOption = event.target;
    const gender = selectedGenderOption.textContent.trim()
    
    customGenderSelect.classList.remove("open");
    selectGenderHeader.textContent = gender;

    document.querySelector('input[name="gender"]').value = gender.toLowerCase();

};


const gender_options = document.querySelectorAll(".gender-option");



// CLICK OUTSIDE FUNCTION

function click_outside(event) {

    
    if (!customGenderSelect.contains(event.target) && customGenderSelect.classList.contains("open")) {
        customGenderSelect.classList.remove("open");
    }
}

// APPLYING FUNCTIONS

selectGenderHeader.addEventListener("click", toggle_dropdown_gender);

document.addEventListener("click", click_outside);


gender_options.forEach(gender_option => {gender_option.addEventListener("click", select_gender_option);

});

