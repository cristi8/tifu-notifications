
// Names are reversed to hide the github repo from google searches of player names

var REVERSED_NAMES = [
    "uiorazaL dalV",
    "eboB anA",
    "naciuB aeerdnA",
    "uionaP nadgoB",
    "ucledeN ierdnA",
    "ucsertimuD aecriM",
    "ucsertimuD anirI",
    "ucraM nailuI",
    "ucsertimuD neguE",
    "salaB naitsirC",
    "illaM bijaN",
    "aderP urdnaxelA",
    "ucselubraS aniretacE",
    "uiotaC uitneruaL",
    "unaetsetreB udaR",
    "esanaT nairpiC",
    "ucseniraM naitsirC",
    "ietaM leirbaG",
    "uranidarG anomiS",
    "vonavI ailemaC",
    "vonavI nailuI",
    "unaiJ tunafetS",
    "tnilaB olzsaL",
    "aecoS aculaR",
    "utrucS ierdnA",
    "iertepA anilA",
    "atnaM aecriM",
    "aecnaO alebasI",
    "recluC anirI",
    "tanreC nadgoB",
    "tanreC ailuI",
    "redeV aeerdnA",
    "uioilI sogarD",
    "soboT lenirI",
    "utiN navzaR",
    "ihciB nilataC",
    "ealociN nirolF",
    "nivaS iahiM",
    "abaH aeerdnA",
    "aerolF ierdnA",
    "uigaoB nadgoB",
    "enoT xelA",
    "alianaD tunoI",
    "naejeL siroL",
    "iilitniP aivliS",
    "acsunA aniladaM",
    "zerheM demhA",
    "niraM anitnelaV",
    "unaierdnA luaP ierdnA",
    "ietaM nilataC",
    "hsraM hciR",
    "unasihcraP iahiM",
    "elisaV nitnelaV",
    "niteleT nadgoB",
    "ucselevaP nairdA",
    "abaH naitsirC",
    "uratoboiC ietaM",
    "unaiovaZ urdnaxelA",
    "ucselirvaG urdnaxelA",
    "ealuceN nimsoC",
    "cutuB naitsirC",
    "kruT uidualC treboR",
    "unaioroM naicuL nairpiC",
    "icialK anelE",
    "alurD nafetS",
    "acriT anelE aivliS",
    "unaenasuR anelE ardnaxelA",
    "yntovoN urdnaxelA nimsoC",
    "anihcoiC anelE aruA",
    "utazuB nirolF",
    "uranidarG neguE",
    "ucseluriP uirelaV ierdnA",
    "uvihC leunamE nilA",
    "notnA nilataC",
    "uciaB nirolF",
    "unapS eniledA",
    "rehgnaoB leirbaG"
];
 

function reverseString(str) {
    return str.split("").reverse().join("");
}

NAMES = [];
for (let i in REVERSED_NAMES) {
    NAMES.push(reverseString(REVERSED_NAMES[i]))
}
NAMES.sort();