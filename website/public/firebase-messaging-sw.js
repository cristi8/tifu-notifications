importScripts("https://www.gstatic.com/firebasejs/7.8.1/firebase-app.js");
importScripts("https://www.gstatic.com/firebasejs/7.8.1/firebase-messaging.js");

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
