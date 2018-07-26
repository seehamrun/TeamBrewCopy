fetch("https://api.worldweatheronline.com/premium/v1/weather.ashx?key=" + weather_key + "&q=60607&format=json&num_of_days=1")
  .then(function(response) {
    response.json().then(function(data) {
      console.log(data);
      currentTemp = data.data.current_condition[0].temp_F
      currentCondition = data.data.current_condition[0].weatherDesc[0].value
      pic.innerHTML = "<h1><img src='" + data.data.current_condition[0].weatherIconUrl[0].value + "'/></h1>"
      bottomTemp.innerHTML = "<p>" + currentTemp + "F</p>"

      jQuery.get("/?temp=" + currentTemp + "&condition=" + currentCondition, () => {
        //alert("Sent")
      })

    });
  })

  var currentGifUrl = null;
  // Makes the element with ID 'resultPane' visible, and sets the element with ID
  // 'result' to contain resultJson


  // contacts our server, and asks it to add gifUrl to the list of favorite GIFs.
  // doneCallback should be a function, which addGifToFavorites will invoke when
  // the gifUrl is saved successfully.
  function addGifToFavorites(doneCallback) {
    var zipcode= document.querySelector('#zip').value;
    jQuery.post("/", {zipcode}, (result) => {
      var zipstuff = document.querySelector()
      console.log(result)
      alert()
    });

    console.log(zipcode)
  }

  // TODO: Create an event handler for when the button is clicked
  // that calls queryGiphy using the displayResult function as the callback

  function submitClick() {
    addGifToFavorites(() => {
      alert("saved")
  })
  }


  window.addEventListener('load', () => {
    document.querySelector('#submit').addEventListener("click", submitClick)
  });
