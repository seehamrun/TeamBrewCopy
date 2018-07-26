// Makes the element with ID 'resultPane' visible, and sets the element with ID
// 'result' to contain resultJson 
// contacts our server, and asks it to add gifUrl to the list of favorite GIFs.
// doneCallback should be a function, which addGifToFavorites will invoke when
// the gifUrl is saved successfully.
function addGifToFavorites(doneCallback) {
  var top = document.querySelector('#tops').value;
  var bottom= document.querySelector('#bottoms').value;
  jQuery.post("/list_favorite", {top, bottom}, doneCallback);
}
function addOutfitToHistory(doneCallback){
  var today = new Date();
  var top = document.querySelector('#tops').value;
  var bottom= document.querySelector('#bottoms').value;
  jQuery.post("/calendar", {today, top, bottom}, doneCallback);
}
// TODO: Create an event handler for when the button is clicked
// that calls queryGiphy using the displayResult function as the callback

function submitClick() {
  addGifToFavorites(()=>{
    alert("saved")
  })
}

function woreClick(){
  addOutfitToHistory( ()=> {
    alert('yay')
  })
}

window.addEventListener('load', () => {
  document.querySelector('#submit').addEventListener("click", submitClick)
  document.querySelector('#worn').addEventListener("click", woreClick)
});
