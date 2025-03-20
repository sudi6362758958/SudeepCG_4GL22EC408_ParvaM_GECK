function validateForm(event) {
    event.preventDefault();

    const formField = document.querySelectorAll("#registration_form .form-control, #registration_form .form-check-input");
    let isvalid = true;

    function createErrorMessage(parentDiv, message) {
        const errorMessage = document.createElement("div");     // Create a <div</div> element
        errorMessage.textContent = message; 
        errorMessage.classList.add("text-danger");     //<div class="text-danger"></div>
        errorMessage.innerText = message;             //<div class="text-danger">`${message}`</div>
        parentDiv.appendChild(errorMessage);

        setTimeout(() => {
            errorMessage.remove();
        }, 5000);
    }

    formField.forEach(field => {
        let parentDiv = field.closest(".mb-3");
        const label = parentDiv.querySelector("label");

        const existingError = parentDiv.querySelector(".text-danger");
        if (existingError) {
            existingError.remove();
        }


        if (field.id === 'phone_number') {
            const phonePattern = /^[6-9]\d{9}$/;
            if (field.value && !phonePattern.test(field.value.trim())) {
                isvalid = false;
                createErrorMessage(parentDiv, 'phone number should contain only 10 digits and should start with(6,7,8 or 9).');
            }
        }

        if (field.id === 'email_id') {
            const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
            if (field.value && !emailPattern.test(field.value.trim())) {
                isvalid = false;
                createErrorMessage(parentDiv, 'Please enter a valid email address.');
            }
        }

        if (field.id === 'aadhar_number') {
            const adharPattern = /^\d{12}$/;
            if (field.value && !adharPattern.test(field.value.trim())) {
                isvalid = false;
                createErrorMessage(parentDiv, 'Aadhar number should contain only 12 digits.');
            }
        }

        if (field.id === 'pin_code') {
            const adharPattern = /^\d{6}$/;
            if (field.value && !adharPattern.test(field.value.trim())) {
                isvalid = false;
                createErrorMessage(parentDiv, 'pin-code should contain only 6 digits.');
            }
        }

        if (label && label.textContent.toLowerCase().includes('name')) {
            const namePattern = /^[a-zA-Z\s]+$/;
            if (field.value && !namePattern.test(field.value.trim())) {
                isvalid = false;
                createErrorMessage(parentDiv, `${label.textContent} Name should contain only alphabets, space & full-stop(period symbol).`);
            }
        }

        if (label && label.textContent.toLowerCase().includes('board')) {
            const namePattern = /^[a-zA-Z\s]+$/;
            if (field.value && !namePattern.test(field.value.trim())) {
                isvalid = false;
                createErrorMessage(parentDiv, `${label.textContent} Name should contain only alphabets, space & full-stop(period symbol).`);
            }
        }

        if (field.type === 'radio' || field.type === 'checkbox') {
            const radiochecked = document.querySelector(`input[name="${field.name}"]:checked`);
            if (!radiochecked) {
                isvalid = false;
                createErrorMessage(parentDiv, ` ${label.textContent} is required field.`);
            }
        } else if (field.value.trim() === '') {
            isvalid = false;
            createErrorMessage(parentDiv, `${label.textContent} is required field.`);
        }
    });

    if (isvalid) {
        alert("Form submitted successfully!");
        document.getElementById("registration_form").submit();
        return true;
    } else {
        return false;
    }
}
