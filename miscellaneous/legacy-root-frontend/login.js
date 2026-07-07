const loginForm = document.querySelector("#loginForm");
const nameInput = document.querySelector("#name");
const emailInput = document.querySelector("#email");
const passwordInput = document.querySelector("#password");
const authModeButtons = document.querySelectorAll("[data-auth-mode]");
const authStatusText = document.querySelector("#authStatus");
const localDemoButton = document.querySelector("#localDemoButton");
const primaryLoginButton = document.querySelector(".primary-button");
const registerOnlyFields = document.querySelectorAll(".register-only");

const isLocalFrontend =
  window.location.protocol === "file:" ||
  window.location.hostname === "127.0.0.1" ||
  window.location.hostname === "localhost";

const configuredBackendUrl = (window.BYTEBOT_BACKEND_URL || "").trim();
const defaultBackendUrl = isLocalFrontend
  ? "http://127.0.0.1:8010"
  : window.location.origin;
const backendUrl = configuredBackendUrl || defaultBackendUrl;

let currentAuthMode = "login";
let backendAuthConfig = {
  mongo_enabled: false
};

if (loginForm && emailInput && passwordInput) {
  loadSavedEmail();
  setupAuthModeButtons();
  setupLocalDemoButton();
  checkBackendAuthConfig();
  loginForm.addEventListener("submit", handleAuthSubmit);
}

function loadSavedEmail() {
  const savedEmail = localStorage.getItem("bytebot_user_email");

  if (savedEmail) {
    emailInput.value = savedEmail;
  }
}

function setupAuthModeButtons() {
  authModeButtons.forEach((button) => {
    button.addEventListener("click", () => {
      setAuthMode(button.dataset.authMode);
    });
  });
}

function setAuthMode(newMode) {
  currentAuthMode = newMode;

  authModeButtons.forEach((button) => {
    button.classList.toggle("is-active", button.dataset.authMode === newMode);
  });

  registerOnlyFields.forEach((field) => {
    field.classList.toggle("is-hidden", newMode !== "register");
  });

  if (primaryLoginButton) {
    primaryLoginButton.textContent = newMode === "register"
      ? "Create Byte-Bot Account"
      : "Sign In To Byte-Bot";
  }
}

function setupLocalDemoButton() {
  localDemoButton?.addEventListener("click", () => {
    const email = emailInput.value.trim() || "guest@local.test";
    const userLabel = makeUserLabel(email);

    saveFrontendSession({
      accessToken: "",
      email,
      userLabel,
      sessionId: `bytebot-${userLabel}`
    });
  });
}

async function checkBackendAuthConfig() {
  try {
    const configResponse = await fetch(`${backendUrl}/auth/config`);

    if (!configResponse.ok) {
      throw new Error(`Auth config returned ${configResponse.status}`);
    }

    backendAuthConfig = await configResponse.json();

    if (backendAuthConfig.mongo_enabled) {
      showStatus("MongoDB auth is ready. Login or register to continue.", false, true);
      localDemoButton?.classList.remove("is-visible");
    } else {
      showStatus("MongoDB is not configured yet. You can still use local demo mode.", true);
      localDemoButton?.classList.add("is-visible");
    }

  } catch (error) {
    console.error("Byte-Bot auth config error:", error);
    showStatus(`Could not reach backend auth at ${backendUrl}. Start FastAPI or use local demo mode.`, true);
    localDemoButton?.classList.add("is-visible");
  }
}

async function handleAuthSubmit(event) {
  event.preventDefault();

  if (!backendAuthConfig.mongo_enabled) {
    showStatus("Real login needs MongoDB. Add MONGODB_URI, restart FastAPI, or use local demo mode.", true);
    localDemoButton?.classList.add("is-visible");
    return;
  }

  const email = emailInput.value.trim();
  const password = passwordInput.value.trim();
  const name = nameInput?.value.trim();

  if (!email || !password) {
    showStatus("Please enter both email and password.", true);
    return;
  }

  const authPath = currentAuthMode === "register" ? "/auth/register" : "/auth/login";
  const requestBody = currentAuthMode === "register"
    ? { email, password, name }
    : { email, password };

  try {
    showStatus("Talking to Byte-Bot backend...", false);
    const authData = await sendAuthRequest(authPath, requestBody);
    saveBackendSession(authData);
  } catch (error) {
    showStatus(error.message, true);
  }
}

async function sendAuthRequest(authPath, requestBody) {
  const response = await fetch(`${backendUrl}${authPath}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(requestBody)
  });

  const responseData = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(responseData.detail || `Backend returned ${response.status}`);
  }

  return responseData;
}

function saveBackendSession(authData) {
  const user = authData.user;
  const userLabel = makeUserLabel(user.email);

  saveFrontendSession({
    accessToken: authData.access_token,
    email: user.email,
    userLabel,
    sessionId: authData.session_id
  });
}

function saveFrontendSession({ accessToken, email, userLabel, sessionId }) {
  localStorage.setItem("bytebot_access_token", accessToken);
  localStorage.setItem("bytebot_user_email", email);
  localStorage.setItem("bytebot_user_label", userLabel);
  localStorage.setItem("bytebot_session_id", sessionId);
  localStorage.setItem("bytebot_api_base_url", backendUrl);

  window.location.href = "chat.html";
}

function makeUserLabel(email) {
  return email
    .split("@")[0]
    .replace(/[^a-z0-9_-]/gi, "-")
    .toLowerCase() || "guest";
}

function showStatus(message, isError = false, isSuccess = false) {
  if (!authStatusText) {
    return;
  }

  authStatusText.textContent = message;
  authStatusText.classList.toggle("is-error", isError);
  authStatusText.classList.toggle("is-success", isSuccess);
}
