    $(function(){
        var dropdown = {
            country: $('#trip_country'),
            city: $('#trip_city')
        };
        updateCities();
        function updateCities() {

            dropdown.city.attr('disabled', 'disabled');
            dropdown.city.empty();

            $.getJSON("/trips/get_cities/", {country: dropdown.country.val()}, function(data) {
                data.forEach(function(item){
                   dropdown.city.append(
                       $('<option>', {
                           value: item[0],
                           text: item[1]
                       })
                   );
                });
                dropdown.city.removeAttr('disabled');
            });
        }
        dropdown.country.on('change', function(){
            updateCities();
        });
    });
