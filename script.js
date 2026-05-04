function addToCart(name, price, image) {
  const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";

  if (!isLoggedIn) {
    alert("Please login to add items to your cart.");
    window.location.href = "login.html";
    return;
  }
  let cart = JSON.parse(localStorage.getItem("myCart")) || [];
  const existingItemIndex = cart.findIndex((item) => item.name === name);

  if (existingItemIndex > -1) {
    cart[existingItemIndex].quantity += 1;
  } else {
    const product = {
      name: name,
      price: price,
      image: image,
      quantity: 1,
    };
    cart.push(product);
  }
  localStorage.setItem("myCart", JSON.stringify(cart));
  updateNavbar();
}
document.addEventListener("DOMContentLoaded", function () {
  updateNavbar();
});

function updateNavbar() {
  const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";
  const navbarRight = document.getElementById("navbar-actions");

  if (isLoggedIn) {
    let cart = JSON.parse(localStorage.getItem("myCart")) || [];
    let totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);

    navbarRight.innerHTML = `
            <a href="cart.html" class="cart-btn">Cart (${totalItems})</a>
            <button onclick="logoutUser()" class="btn-logout">Logout</button>
        `;
  } else {
    navbarRight.innerHTML = `
            <a href="login.html" class="auth-link">Login</a>
            <a href="login.html" class="auth-btn-alt">Sign Up</a>
        `;
  }
}

function logoutUser() {
  localStorage.removeItem("isLoggedIn");
  window.location.href = "index.html";
}
