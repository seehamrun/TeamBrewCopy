var feedback = function(res) {
    if (res.success === true) {
        var get_link = res.data.link.replace(/^http:\/\//i, 'https://');
        document.querySelector('.status').classList.add('bg-success');
        document.querySelector('.status').innerHTML =
            'Image : ' + '<br><input class="image-url" value=\"' + get_link + '\"/>' + '<img class="img" alt="Imgur-Upload" src=\"' + get_link + '\"/>';
		
    }
};

new Imgur({
    clientid: 'ea32dd4d0404854', //You can change this ClientID
    callback: feedback
});


var currentGifUrl = null;

// Makes the element with ID 'resultPane' visible, and sets the element with ID
// 'result' to contain resultJson
function displayResult(resultJson) {
  var resultPaneDiv = document.querySelector('#resultPane')
  var resultDiv = document.querySelector('#result')

  currentGifUrl = resultJson.data[0].images.downsized.url;
  
  var imgString = "<img src='" +
                  resultJson.data[0].images.downsized.url +
                  "'/>"
  resultDiv.innerHTML = imgString

  // This line makes the container for the result div and the "add to favorites"
  // button visible.
  resultPaneDiv.style.display = "block"
}

// contacts our server, and asks it to add gifUrl to the list of favorite GIFs.
// doneCallback should be a function, which addGifToFavorites will invoke when
// the gifUrl is saved successfully.
function addGifToFavorites(doneCallback) {
  jQuery.post("/add_favorite", get_link, doneCallback);
}

// TODO: Create an event handler for when the button is clicked
// that calls queryGiphy using the displayResult function as the callback

function submitClick() {
	  alert('Yay! You saved!')
}


window.addEventListener('load', () => {
  document.querySelector('#submit').addEventListener("click", submitClick)
});
