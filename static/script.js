
const sendButton = document.getElementById("sendRequest");
const statusElement = document.getElementById("status");
const responseElement = document.getElementById("response");

sendButton.addEventListener("click", async () => {

    const user = document.getElementById("user").value;
    const mode = document.getElementById("mode").value;
    const documentId = document.getElementById("document").value;

    const url = `/${mode}/documents/${documentId}`;

    // Simulated authentication
    const token = `${user}-token`;

    statusElement.textContent = "Status: Loading...";

    try {
        const response = await fetch(url, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await response.json();

        statusElement.textContent =
            `Status: ${response.status} ${response.statusText}`;

        responseElement.textContent =
            JSON.stringify(data, null, 4);

        if (response.ok) {
            statusElement.style.color = "#86efac";
        } else {
            statusElement.style.color = "#f87171";
        }

    } catch (error) {
        statusElement.textContent = "Connection error";
        statusElement.style.color = "#f87171";
        responseElement.textContent = error.message;
    }
});
