fetch("https://api.worldweatheronline.com/premium/v1/weather.ashx?key=" + weather_key + "&q=60607&format=json&num_of_days=1")
  .then(function(response) {
    response.json().then(function(data) {
      console.log(data);
      currentTemp = data.data.current_condition[0].temp_F
      currentCondition = data.data.current_condition[0].weatherDesc[0].value
      temp.innerHTML = "<h1>The current weather is " + currentTemp + "F</h1>"
      pic.innerHTML = "<img src='" + data.data.current_condition[0].weatherIconUrl[0].value + "'/>"

      jQuery.get("/?temp=" + currentTemp + "&condition=" + currentCondition, () => {
        //alert("Sent")
      })

    });
  })
