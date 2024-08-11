// Ensure the DOM is fully loaded before executing the function
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

    // Perform an AJAX GET request to check the status of the API
    $.getJSON("http://0.0.0.0:5001/api/v1/status/", (data) => {
        // If the status from the API response is "OK", add the "available" class to the #api_status div
        if (data.status === "OK") {
            $("div#api_status").addClass("available");
        } else {
            // Otherwise, remove the "available" class from the #api_status div
            $("div#api_status").removeClass("available");
        }
    });
});

