document.addEventListener("DOMContentLoaded", () => {
    if(localStorage.getItem("trueprofit_vip") === "true") {
        document.querySelectorAll("div.fixed, .backdrop-blur-sm, [style*='z-index: 50']").forEach(el => el.style.display = "none");
    }

    document.querySelectorAll("button").forEach(btn => {
        if(btn.textContent.includes("Log In") || btn.textContent.includes("Verify")) {
            btn.onclick = (e) => {
                e.preventDefault();
                const email = prompt("TRUEPROFIT™ Secure Login\n\nEnter your authorized email:");
                
                if (email && email.trim().toLowerCase() === "hummuahmad@gmail.com") {
                    alert("VIP Master Key accepted. Welcome, CEO.");
                    localStorage.setItem("trueprofit_vip", "true");
                    document.querySelectorAll("div.fixed, .backdrop-blur-sm, [style*='z-index: 50']").forEach(el => el.style.display = "none");
                } else if (email) {
                    alert("Access Denied. Email not authorized.");
                }
            };
        }
    });
});
