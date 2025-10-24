document.addEventListener('DOMContentLoaded', function() {
    const isAthleteField = document.querySelector('#id_is_athlete');
    const isCoachField = document.querySelector('#id_is_coach');
    const athleteFields = document.querySelectorAll('.field-weight, .field-belt, .field-category, .field-coach');
    const coachFields = document.querySelectorAll('.field-level');

    function toggleFields() {
        if (isAthleteField.checked) {
            athleteFields.forEach(field => field.style.display = 'block');
            coachFields.forEach(field => field.style.display = 'none');
        } else if (isCoachField.checked) {
            athleteFields.forEach(field => field.style.display = 'none');
            coachFields.forEach(field => field.style.display = 'block');
        } else {
            athleteFields.forEach(field => field.style.display = 'none');
            coachFields.forEach(field => field.style.display = 'none');
        }
    }

    isAthleteField.addEventListener('change', toggleFields);
    isCoachField.addEventListener('change', toggleFields);

    // Initial call to set the correct visibility on page load
    toggleFields();
});
