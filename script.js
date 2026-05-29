console.log("Script läuft!");

const API = "https://birthdaygift-backend.onrender.com/api/rezensionen";  /* Adresse von Backend */

/* Side navigation */
function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

/* Load reviews */
async function loadReviews() {
    try {
        const res = await fetch(API);                 /* Schickt Anfrage an Backend*/ 

        if (!res.ok) {                                   /*Abbruch falls Fehler */
            console.error("API Fehler:", res.status);
            return;
        }

        const data = await res.json();                  /**liest daten aus */

        const container = document.getElementById("reviews");       /*erstellt html container für review und löscht alte einträge*/
        container.innerHTML = "";

data.forEach(r => {

    const div = document.createElement("div");
    div.className = "card";

    const body = document.createElement("div");
    body.className = "card-body";

    const user = document.createElement("div");
    user.className = "review-user";
    user.textContent = r.user || "Anonym";

    const content = document.createElement("div");
    content.className = "review-content";
    content.textContent = r.content;

    const date = document.createElement("div");
    date.className = "review-date";
    date.textContent = new Date(r.created_at).toLocaleString();

    body.appendChild(user);
    body.appendChild(content);
    body.appendChild(date);

    div.appendChild(body);

    container.appendChild(div);
});

    } catch (err) {
        console.error("Fetch Fehler:", err);
    }
}

/* Form handler */
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form");

    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const input = document.getElementById("input2");
        const name = document.getElementById("input1")
        const content = input.value;
        const user = name.value;


        await fetch(API, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ content, user})
        });

        input.value = "";
        name.value = "";
        loadReviews();
    });

    loadReviews();
});