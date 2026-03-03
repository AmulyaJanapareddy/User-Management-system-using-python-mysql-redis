const API_BASE_URL = "http://localhost:8000";

const addUserBtn = document.getElementById("addUserBtn");
const fetchMySQLBtn = document.getElementById("fetchMySQLBtn");
const fetchRedisBtn = document.getElementById("fetchRedisBtn");

const userIdInput = document.getElementById("userId");
const userNameInput = document.getElementById("userName");
const userMobileInput = document.getElementById("userMobile");

const addUserMessage = document.getElementById("addUserMessage");
const resultsContainer = document.getElementById("resultsContainer");
const sourceInfo = document.getElementById("sourceInfo");
const fetchTimeInfo = document.getElementById("fetchTimeInfo");
const usersList = document.getElementById("usersList");

addUserBtn.addEventListener("click", addUser);
fetchMySQLBtn.addEventListener("click", fetchFromMySQL);
fetchRedisBtn.addEventListener("click", fetchFromRedis);

async function addUser() {
    const id = parseInt(userIdInput.value);
    const name = userNameInput.value.trim();
    const mobile = userMobileInput.value.trim();

    if (!id || !name || !mobile) {
        showMessage("Please fill in all fields", "error");
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/createuser`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                id: id,
                name: name,
                mobile: mobile,
            }),
        });

        const data = await response.json();

        if (response.ok) {
            showMessage(data.message, "success");
            userIdInput.value = "";
            userNameInput.value = "";
            userMobileInput.value = "";
            userIdInput.focus();
        } else {
            showMessage(data.detail || "Error adding user", "error");
        }
    } catch (error) {
        showMessage("Error: " + error.message, "error");
    }
}

async function fetchFromMySQL() {
    try {
        const response = await fetch(`${API_BASE_URL}/users/mysql`);
        const data = await response.json();

        if (response.ok) {
            displayResults(data);
        } else {
            showMessage(data.detail || "Error fetching from MySQL", "error");
        }
    } catch (error) {
        showMessage("Error: " + error.message, "error");
    }
}

async function fetchFromRedis() {
    try {
        const response = await fetch(`${API_BASE_URL}/users/redis`);
        const data = await response.json();

        if (response.ok) {
            displayResults(data);
        } else {
            showMessage(data.detail || "Error fetching from Redis", "error");
        }
    } catch (error) {
        showMessage("Error: " + error.message, "error");
    }
}

function displayResults(data) {
    sourceInfo.textContent = `Source: ${data.source}`;
    fetchTimeInfo.textContent = `Fetch Time: ${data.fetch_time}`;

    usersList.innerHTML = "";

    if (data.users && data.users.length > 0) {
        data.users.forEach((user) => {
            const userCard = document.createElement("div");
            userCard.className = "user-card";
            userCard.innerHTML = `
                <h3>${user.name}</h3>
                <div class="user-info">
                    <span><strong>ID:</strong> ${user.id}</span>
                    <span><strong>Mobile:</strong> ${user.mobile}</span>
                </div>
            `;
            usersList.appendChild(userCard);
        });
    } else {
        usersList.innerHTML =
            '<div class="empty-state"><p>No users found</p></div>';
    }

    resultsContainer.classList.remove("hidden");
}

function showMessage(message, type) {
    addUserMessage.textContent = message;
    addUserMessage.className = `message ${type}`;

    if (type === "success") {
        setTimeout(() => {
            addUserMessage.className = "message";
        }, 3000);
    }
}
