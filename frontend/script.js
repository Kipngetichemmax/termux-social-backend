let token = "";

// ----- Register -----
async function register() {
  const username = document.getElementById("reg-username").value;
  const email = document.getElementById("reg-email").value;
  const password = document.getElementById("reg-password").value;

  const res = await fetch("http://127.0.0.1:5000/api/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email, password })
  });
  const data = await res.json();
  alert(JSON.stringify(data));
}

// ----- Login -----
async function login() {
  const username = document.getElementById("login-username").value;
  const password = document.getElementById("login-password").value;

  const res = await fetch("http://127.0.0.1:5000/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });
  const data = await res.json();
  if (data.token) token = data.token;
  alert(JSON.stringify(data));
}

// ----- Create Post -----
async function createPost() {
  const content = document.getElementById("post-content").value;

  const res = await fetch("http://127.0.0.1:5000/api/posts/create", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + token
    },
    body: JSON.stringify({ content })
  });

  const data = await res.json();
  alert(JSON.stringify(data));
  loadFeed();
}

// ----- Load Feed -----
async function loadFeed() {
  const res = await fetch("http://127.0.0.1:5000/api/posts/", {
    method: "GET",
    headers: { "Authorization": "Bearer " + token }
  });
  const data = await res.json();
  const feedEl = document.getElementById("feed");
  feedEl.innerHTML = "";
  data.forEach(post => {
    const li = document.createElement("li");
    li.textContent = `${post.user.username}: ${post.content}`;
    feedEl.appendChild(li);
  });
}

// Load feed on page load
window.onload = loadFeed;
