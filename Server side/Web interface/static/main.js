// main.js

const url = "/get_icd_data";
const payload = {
    client_id: "f4a39ebe-734c-4fb2-8b5d-ac36a670708f_0782aa93-3766-474c-aeb8-04b1e82f3f6f",
    client_secret: "/0/VmvmGmdePAKyzO6gx52AhAkjw/KTAsrpkBKRe66I="
};

fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
})
.then(response => {
    if (response.ok) {
        return response.json();
    } else {
        throw new Error(`Error: ${response.statusText}`);
    }
})
.then(responseText => {
    console.log(responseText);
    const idElement = document.getElementById("icd_id");
    const titleElement = document.getElementById("icd_title");
    const definitionElement = document.getElementById("icd_definition");

    idElement.textContent = responseText["@id"];
    titleElement.textContent = responseText.title["@value"];
    definitionElement.textContent = responseText.definition["@value"];
})
.catch(error => {
    console.log(error);
});
