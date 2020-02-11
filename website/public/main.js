// Your web app's Firebase configuration
var firebaseConfig = {
apiKey: "AIzaSyAXOWBDp4p35y6T3v4Mqlih9i8vzt-pCBE",
    authDomain: "tifu-notifications.firebaseapp.com",
    databaseURL: "https://tifu-notifications.firebaseio.com",
    projectId: "tifu-notifications",
    storageBucket: "tifu-notifications.appspot.com",
    messagingSenderId: "169626025455",
    appId: "1:169626025455:web:200b59ecc9a13940e74a1a"
};
firebase.initializeApp(firebaseConfig);

const messaging = firebase.messaging();

messaging.requestPermission().then(function() {
    console.log("Got notification permissions");
    return messaging.getToken();
})
.then(function(token) {
    console.log(token);
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "http://localhost:8080/register", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("token=" + encodeURIComponent(token) + "&name=" + encodeURIComponent("hello"));
})
.catch(function(err) {
    console.log("Error: ", err);
});

messaging.onMessage(function(payload) {
    console.log("onMessage: ", payload);
});
