function selectService(service) {
    document.getElementById("service").value = service;
    loadProviders();
}

// Book service
async function bookService() {
    const name = document.getElementById("name").value;
    const location = document.getElementById("location").value;
    const service = document.getElementById("service").value;

    const response = await fetch("/book", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, location, service })
    });

    const data = await response.json();
    alert(data.message);
    loadProviders(); // Refresh providers
}

// Load providers for selected service
async function loadProviders() {
    const service = document.getElementById("service").value;
    const response = await fetch(`/providers/${service}`);
    const providers = await response.json();

    let output = "";
    providers.forEach(p => {
        output += `
            <div class="provider-card">
                <h3>${p[1]}</h3>
                <p>Phone: ${p[3]}</p>
                <p>Location: ${p[4]}</p>
                <p>Experience: ${p[5]}</p>
                <p>Price: ${p[6]}</p>
                <p>Status: ${p[7]}</p>
                <button onclick="callProvider('${p[3]}')">📞 Call</button>
                <button onclick="whatsappProvider('${p[3]}')">💬 WhatsApp</button>
            </div>
        `;
    });

    document.getElementById("providersList").innerHTML = output;
}

// Call provider
function callProvider(phone) {
    window.location.href = `tel:${phone}`;
}

// WhatsApp chat
function whatsappProvider(phone) {
    window.open(`https://wa.me/91${phone}`);
}

// Load initial providers
window.onload = loadProviders;