
var firebaseConfig = {
    apiKey: "AIzaSyAXOWBDp4p35y6T3v4Mqlih9i8vzt-pCBE",
    authDomain: "tifu-notifications.firebaseapp.com",
    databaseURL: "https://tifu-notifications.firebaseio.com",
    projectId: "tifu-notifications",
    storageBucket: "tifu-notifications.appspot.com",
    messagingSenderId: "169626025455",
    appId: "1:169626025455:web:200b59ecc9a13940e74a1a"
};

var messaging;

function initFirebase() {
    firebase.initializeApp(firebaseConfig);

    messaging = firebase.messaging();
    messaging.usePublicVapidKey("BK7rdAzU3Z6hZ-ronmsnAiLKxOssmGhJzAdcCkjhibDr5KJiTARATOHvoc2iGXNGHNG1UIdKCISjtl6dunT_UgI");

    firebase.notifications().onNotification((notification) => {
        console.log("onNotification", notification);
        firebase.notifications().displayNotification(notification);
    });

    messaging.onMessage(function(payload) {
        console.log("onMessage: ", payload);


        //let notification = new Notification(
        //    payload.notification.title,
        //    payload.notification
        //);
    });

}


function setStatus(status) {
    $('.status').text(status);
}

function setUIState(name, state) {
    let allPlayers = $('.player-name');
    let targetPlayer = $('.player-name').filter(function() { return $(this).text() == name});
    allPlayers.removeClass('state-busy state-success state-error');
    targetPlayer.addClass('state-' + state);
}


function registerAs(name) {
    setStatus("Obtaining notification user token...");
    setUIState(name, 'busy');

    messaging.getToken().then((token) => {
        console.log(token);

        setStatus("Registering as '" + name + "'...");
        $.post("/api/register", {
                token: token,
                name: name
            }, function(data) {
                setStatus("Registered successfully as '" + name + "'.");
                setUIState(name, 'success');
            }
        ).fail(function(xhr, p2, p3) {
            var errorMessage = xhr.status + ': ' + xhr['statusText'];
            setStatus("Server communication error: " + errorMessage);
            setUIState(name, 'error');
        });
        })
    .catch(function(err) {
        setStatus("ERROR: " + err);
        setUIState(name, 'error');
    });

}

function uiClicked(domElement) {
    let name = $(domElement).text();
    registerAs(name);
}

function initUI() {
    for (let i in NAMES) {
        let div = $('<div />', {
            class: "player-name",
            text: NAMES[i],
            click: function(e) {
                uiClicked(this);
            }
        });
        $('#name-collection').append(div);
    }
}

$(() => {
    try {
        setStatus("Initializing firebase...");
        initFirebase();
        setStatus("Initializing UI...");
        initUI();
        setStatus("");
    } catch(err) {
        $('#content').empty();
        setStatus("Error: " + err);
    }
})
