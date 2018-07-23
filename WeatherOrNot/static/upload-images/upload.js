var currentGifUrl = null;
var feedback = function(res) {
    if (res.success === true) {
        var get_link = res.data.link.replace(/^http:\/\//i, 'https://');
        document.querySelector('.status').classList.add('bg-success');
        document.querySelector('.status').innerHTML =
            'Image : ' + '<br><input class="image-url" value=\"' + get_link + '\"/>' + '<img class="img" alt="Imgur-Upload" src=\"' + get_link + '\"/>';

    }
    currentGifUrl=get_link
};

new Imgur({
    clientid: "ea32dd4d0404854", //You can change this ClientID
    callback: feedback
});



// Makes the element with ID 'resultPane' visible, and sets the element with ID
// 'result' to contain resultJson


// contacts our server, and asks it to add gifUrl to the list of favorite GIFs.
// doneCallback should be a function, which addGifToFavorites will invoke when
// the gifUrl is saved successfully.
function addGifToFavorites(input_url, doneCallback) {
  var type = document.querySelector('#type').value;
  var materials= document.querySelector('#materials').value;
  var length =document.querySelector('#length').value;
  jQuery.post("/add_item", {url:input_url, type, length, materials}, doneCallback);
}

// TODO: Create an event handler for when the button is clicked
// that calls queryGiphy using the displayResult function as the callback

function submitClick() {
  addGifToFavorites(currentGifUrl, () => {
    alert("saved")
})

}


window.addEventListener('load', () => {
  document.querySelector('#submit').addEventListener("click", submitClick)
});
