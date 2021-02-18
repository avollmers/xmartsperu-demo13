var formData = new FormData();
var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
var yyyy = today.getFullYear();

today = mm + '/' + dd + '/' + yyyy;
formData.append(
  "token", "YuA0fYfpjB9CCnGhP7n6U5sQ6ACahY6nzS8iUZoQb4fTMlOxbvB0HSsh54mC",
  "fecha", today
);

var request = new XMLHttpRequest();

request.open("POST", "https://api.migo.pe/api/v1/exchange/date");
request.setRequestHeader("Accept", "application/json");

request.send(formData);
request.onload = function() {
  var data = JSON.parse(this.response);
  console.log(data);
};