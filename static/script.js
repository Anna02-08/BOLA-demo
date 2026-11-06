
const sendButton = document.getElementById("sendRequest");
const resetButton = document.getElementById("resetButton");

const statusElement = document.getElementById("status");
const responseElement = document.getElementById("response");

const methodSelect = document.getElementById("method");
const updateForm = document.getElementById("updateForm");


// Show update form only for PUT requests
methodSelect.addEventListener("change", () => {
    updateForm.style.display =
        methodSelect.value === "PUT" ? "block" : "none";
});

// Send API request
sendButton.addEventListener("click", async () => {

    const user = document.getElementById("user").value;
    const mode = document.getElementById("mode").value;
    const documentId = document.getElementById("document").value;
    const method = methodSelect.value;

    const url = `/${mode}/documents/${documentId}`;
    const token = `${user}-token`;

    const options = {
        method: method,
        headers: {
            "Authorization": `Bearer ${token}`
        }
    };

    // PUT requires JSON body
    if (method === "PUT") {
        const newTitle =
            document.getElementById("newTitle").value;

        options.headers["Content-Type"] = "application/json";
        options.body = JSON.stringify({
            title: newTitle
        });
    }

    statusElement.textContent = "Status: Loading...";

    try {
        const response = await fetch(url, options);
        const contentType = response.headers.get("content-type") || "";

        let data;

        if (contentType.includes("application/json")) {
            data = await response.json();
        } else {
            data = {
                error: `HTTP ${response.status}`,
                message: "Server returned a non-JSON response."
            };
        }

        statusElement.textContent =
            `Status: ${response.status} ${response.statusText}`;

        responseElement.textContent =
            JSON.stringify(data, null, 4);

        statusElement.style.color =
            response.ok ? "#86efac" : "#f87171";

    } catch (error) {
        statusElement.textContent = "Connection error";
        statusElement.style.color = "#f87171";
        responseElement.textContent = error.message;
    }
});

// Restore original documents
resetButton.addEventListener("click", async () => {

    const confirmed = confirm(
        "Restore original demo documents?"
    );

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch("/reset", {
            method: "POST"
        });

        const data = await response.json();

        statusElement.textContent =
            `Status: ${response.status} ${response.statusText}`;

        responseElement.textContent =
            JSON.stringify(data, null, 4);

        statusElement.style.color =
            response.ok ? "#86efac" : "#f87171";

    } catch (error) {
        statusElement.textContent = "Connection error";
        responseElement.textContent = error.message;
    }
});


// Update request in the preview section
function updateRequestPreview() {
    const mode = document.getElementById("mode").value;
    const documentId = document.getElementById("document").value;
    const user = document.getElementById("user").value;

    document.getElementById("endpointPreview").textContent =
        `/${mode}/documents/${documentId}`;

    document.getElementById("authPreview").textContent =
        `Authorization: Bearer ${user}-token`;
}
["mode", "document", "user"].forEach(id => {
    document.getElementById(id).addEventListener(
        "input",
        updateRequestPreview
    );
});

updateRequestPreview();