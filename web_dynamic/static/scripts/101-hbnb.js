$(document).ready(function () {
    // Define the base URL for API requests
    const HOST = "http://127.0.0.1:5001";
    
    // Initialize objects to keep track of selected amenities, cities, and states
    const amenities = {};
    const cities = {};
    const states = {};

    // Attach a change event listener to all checkbox inputs within list items
    $('ul li input[type="checkbox"]').bind("change", (e) => {
        const el = e.target; // Get the checkbox element that triggered the event
        let tt; // Variable to hold the object corresponding to the checkbox type

        // Determine which object (states, cities, amenities) to update based on the checkbox ID
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

        // Update the selected items object based on whether the checkbox is checked or unchecked
        if (el.checked) {
            tt[el.dataset.name] = el.dataset.id;
        } else {
            delete tt[el.dataset.name];
        }

        // Update the display of selected amenities or locations based on the checkbox type
        if (el.id === "amenity_filter") {
            $(".amenities h4").text(Object.keys(amenities).sort().join(", "));
        } else {
            // Combine states and cities into one object and update the locations display
            $(".locations h4").text(
                Object.keys(Object.assign({}, states, cities)).sort().join(", ")
            );
        }
    });

    // Fetch the status of the API to check if it is available
    $.getJSON("http://0.0.0.0:5001/api/v1/status/", (data) => {
        // Update the API status indicator based on the response
        if (data.status === "OK") {
            $("div#api_status").addClass("available");
        } else {
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

    // Attach the searchPlace function to the click event of the search button
    $(".filters button").bind("click", searchPlace);
    // Call searchPlace function to load initial search results
    searchPlace();

    // Function to search for places based on selected filters
    function searchPlace() {
        $.post({
            url: `${HOST}/api/v1/places_search`, // URL to fetch filtered places data
            data: JSON.stringify({
                amenities: Object.values(amenities), // Send selected amenities
                states: Object.values(states), // Send selected states
                cities: Object.values(cities), // Send selected cities
            }),
            headers: {
                "Content-Type": "application/json", // Set content type to JSON
            },
            success: (data) => {
                // Clear previously displayed places
                $("section.places").empty();
                // Log place IDs to the console for debugging
                data.forEach((d) => console.log(d.id));
                // Iterate over each place in the filtered data
                data.forEach((place) => {
                    // Append a new article element with place details and reviews to the section.places element
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
                            <div class="reviews" data-place="${place.id}">
                                <h2></h2>
                                <ul></ul>
                            </div>
                        </article>`
                    );
                    // Fetch and display reviews for the place
                    fetchReviews(place.id);
                });
            },
            dataType: "json", // Expect the response to be in JSON format
        });
    }

    // Function to fetch and display reviews for a given place
    function fetchReviews(placeId) {
        $.getJSON(
            `${HOST}/api/v1/places/${placeId}/reviews`, // URL to fetch reviews for the place
            (data) => {
                // Update the reviews section header with the number of reviews and a toggle button
                $(`.reviews[data-place="${placeId}"] h2`)
                    .text("test")
                    .html(`${data.length} Reviews <span id="toggle_review">show</span>`);
                // Attach a click event listener to the toggle button
                $(`.reviews[data-place="${placeId}"] h2 #toggle_review`).bind(
                    "click",
                    { placeId },
                    function (e) {
                        const rev = $(`.reviews[data-place="${e.data.placeId}"] ul`);
                        if (rev.css("display") === "none") {
                            rev.css("display", "block"); // Show reviews
                            // Fetch and display review details
                            data.forEach((r) => {
                                $.getJSON(
                                    `${HOST}/api/v1/users/${r.user_id}`,
                                    (u) =>
                                        $(".reviews ul").append(`
                                        <li>
                                            <h3>From ${u.first_name + " " + u.last_name} the ${r.created_at}</h3>
                                            <p>${r.text}</p>
                                        </li>`),
                                    "json"
                                );
                            });
                        } else {
                            rev.css("display", "none"); // Hide reviews
                        }
                    }
                );
            },
            "json" // Expect the response to be in JSON format
        );
    }
});

