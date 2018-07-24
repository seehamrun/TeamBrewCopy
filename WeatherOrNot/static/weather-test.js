fetch("https://api.worldweatheronline.com/premium/v1/weather.ashx?key=" + weather_key + "&q=60607&format=json&num_of_days=1")
  .then(function(response) {
    response.json().then(function(data) {
      console.log(data);
      currentTemp = data.data.current_condition[0].temp_F
      temp.innerHTML = "<h1>The current weather is " + currentTemp + "F</h1>"
      condition.innerHTML = "<p>" + data.data.current_condition[0].weatherDesc[0].value + "</p>"
      pic.innerHTML = "<img src='" + data.data.current_condition[0].weatherIconUrl[0].value + "'/>"
    });
  })

jQuery.post("/", {temp: currentTemp}, () => {
  alert("Saved")
})
