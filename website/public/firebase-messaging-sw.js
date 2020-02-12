importScripts("https://www.gstatic.com/firebasejs/7.8.1/firebase-app.js");
importScripts("https://www.gstatic.com/firebasejs/7.8.1/firebase-messaging.js");

firebase.initializeApp({
    appId: "1:169626025455:web:200b59ecc9a13940e74a1a",
    apiKey: "AIzaSyAXOWBDp4p35y6T3v4Mqlih9i8vzt-pCBE",
    projectId: "tifu-notifications",
    messagingSenderId: "169626025455",
});

const messaging = firebase.messaging();
