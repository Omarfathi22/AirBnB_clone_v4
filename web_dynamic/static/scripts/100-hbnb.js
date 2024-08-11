// Ensure the DOM is fully loaded before executing the function
$(document).ready(function () {
    // Define the server host URL
    const HOST = "http://127.0.0.1:5001";

    // Initialize empty objects to store selected amenities, cities, and states
    const amenities = {};
    const cities = {};
    const states = {};

    // Attach a change event listener to all checkbox inputs within list items
    $('ul li input[type="checkbox"]').bind("change", (e) => {
        const el = e.target; // Get the target element of the event
        let tt; // Temporary variable to store the correct filter object

        // Determine which filter object to use based on the checkbox ID
        switch (el.id) {
            case "state_filter":
                tt = states;
                break;
            case "city_filter":
                tt = cities;
                break;
            case "amenity_filter":
                tt = amenities;
                break;
        }

        // Update the filter object based on the checkbox state
        if (el.checked) {
            // Add the checked item to the respective filter object
            tt[el.dataset.name] = el.dataset.id;
        } else {
            // Remove the unchecked item from the respective filter object
            delete tt[el.dataset.name];
        }

        // Update the displayed list based on the filter changes
        if (el.id === "amenity_filter") {
            // Update amenities display with the sorted list of selected amenities
            $(".amenities h4").text(Object.keys(amenities).sort().join(", "));
        } else {
            // Update locations display with the sorted list of selected states and cities
            $(".locations h4").text(
                Object.keys(Object.assign({}, states, cities)).sort().join(", ")
            );
        }
    });

    // Fetch the status of the API to determine if it is available
    $.getJSON("http://0.0.0.0:5001/api/v1/status/", (data) => {
        // If the API status is "OK", add the "available" class to the #api_status div
        if (data.status === "OK") {
            $("div#api_status").addClass("available");
        } else {
            // Otherwise, remove the "available" class from the #api_status div
            $("div#api_status").removeClass("available");
        }
    });

    // Fetch data about places from the server
    $.post({
        url: `${HOST}/api/v1/places_search`, // URL to fetch places data
        data: JSON.stringify({}), // Send an empty JSON object as the request body
        headers: {
            "Content-Type": "application/json", // Set content type to JSON
        },
        success: (data) => {
            // Iterate over each place in the response data
            data.forEach((place) =>
                // Append a new article element with place details to the section.places element
                $("section.places").append(
                    `<article>
                        <div class="title_box">
                            <h2>${place.name}</h2>
                            <div class="price_by_night">$${place.price_by_night}</div>
                        </div>
                        <div class="information">
                            <div class="max_guest">${place.max_guest} Guest${place.max_guest !== 1 ? "s" : ""}</div>
                            <div class="number_rooms">${place.number_rooms} Bedroom${place.number_rooms !== 1 ? "s" : ""}</div>
                            <div class="number_bathrooms">${place.number_bathrooms} Bathroom${place.number_bathrooms !== 1 ? "s" : ""}</div>
                        </div>
                        <div class="description">
                            ${place.description}
                        </div>
                    </article>`
                )
            );
        },
        dataType: "json", // Expect the response to be in JSON format
    });

    // Bind the click event of the search button to the searchPlace function
    $(".filters button").bind("click", searchPlace);
    // Call searchPlace function to load initial search results
    searchPlace();
});

