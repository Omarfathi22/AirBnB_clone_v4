// Wait for the DOM to fully load before executing the function
$(document).ready(function () {
    // Create an empty object to store selected amenities
    const amenities = {};

    // Attach a change event listener to all checkbox inputs within list items
    $("li input[type=checkbox]").change(function () {
        // If the checkbox is checked, add the amenity to the amenities object
        if (this.checked) {
            amenities[this.dataset.name] = this.dataset.id;
        } else {
            // If the checkbox is unchecked, remove the amenity from the amenities object
            delete amenities[this.dataset.name];
        }

        // Update the text inside the amenities <h4> element with the sorted list of selected amenities
        $(".amenities h4").text(Object.keys(amenities).sort().join(", "));
    });
});

