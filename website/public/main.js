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

// messaging.usePublicVapidKey("BK7rdAzU3Z6hZ-ronmsnAiLKxOssmGhJzAdcCkjhibDr5KJiTARATOHvoc2iGXNGHNG1UIdKCISjtl6dunT_UgI");

messaging.requestPermission().then(function() {
    console.log("Got notification permissions");
    return messaging.getToken();
})
.then(function(token) {
    console.log(token);
})
.catch(function(err) {
    console.log("Permission error");
});

messaging.onMessage(function(payload) {
    console.log("onMessage: ", payload);
});
