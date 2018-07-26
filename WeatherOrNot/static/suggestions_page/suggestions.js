currentTemp = ""

fetch("https://api.worldweatheronline.com/premium/v1/weather.ashx?key=" + weather_key + "&q=60607&format=json&num_of_days=1")
  .then(function(response) {
    response.json().then(function(data) {
      console.log(data);
      currentTemp = data.data.current_condition[0].temp_F
      currentCondition = data.data.current_condition[0].weatherDesc[0].value
      currentMaxTemp=data.data.weather[0].maxtempF
      currentMinTemp=data.data.weather[0].mintempF
      // temp.innerHTML = "<h1>The current weather is " + currentTemp + "F</h1>"
      // condition.innerHTML = "<p>" + currentCondition + "</p>"
      // pic.innerHTML = "<img src='" + data.data.current_condition[0].weatherIconUrl[0].value + "'/>"

      jQuery.get("/get_weather?temp=" + currentTemp + "&condition=" + "cloudy" + "&maxTemp=" + currentMaxTemp + "&minTemp=" + currentMinTemp, (clothing) => {
        // alert("Sent")
        console.log(clothing)
        clothing.shirt.forEach((element) => {
          tops.innerHTML += "<img src='" + element + "'/>"
        });

        clothing.pants.forEach((element) => {
          bottoms.innerHTML += "<img src='" + element + "'/>"
        });

        clothing.coat.forEach((element) => {
          coats.innerHTML += "<img src='" + element + "'/>"
        });

        clothing.jacket.forEach((element) => {
          jackets.innerHTML += "<img src='" + element + "'/>"
        });

        clothing.sweater.forEach((element) => {
          sweaters.innerHTML += "<img src='" + element + "'/>"
        });

        clothing.skirt.forEach((element) => {
          skirts.innerHTML += "<img src='" + element + "'/>"
        });

        clothing.dress.forEach((element) => {
          dresses.innerHTML += "<img src='" + element + "'/>"
        });
      })

    });
  })
