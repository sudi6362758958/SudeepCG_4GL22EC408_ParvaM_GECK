const form = document.getElementById("registration_form");
    form.style.backgroundColor = "lightgray";

function validateForm(event){
    event.preventDefault();

    const studentName = document.getElementById("student_name"); 
    const nameError = document.getElementsByClassName("name_error");
    
    if (studentName.value == ''){
        studentName.style.border = "2px solid red";
        nameError[0].textContent = "Name cannot be empty!";
    }
}