(function () {
    "use strict";

    async function loadProducts() {
        var url = "/products/";
        try {
            var response = await fetch(url, {
                headers: { Accept: "application/json" },
            });
            var data = await response.json();

            console.log("[Products API] URL:", url);
            console.log("[Products API] status:", response.status, response.statusText);
            console.log("[Products API] JSON:", data);

            if (data && Array.isArray(data.results)) {
                console.log(
                    "[Products API] Paginated: this page has",
                    data.results.length,
                    "items. Total count:",
                    data.count,
                    "| next:",
                    data.next
                );
            }
        } catch (err) {
            console.error("[Products API] fecth error:", err);
        }
    }

    if (document. readyState == "loading") {
        document.addEventListener("DOMContentLoaded", loadProducts);
    } else {
        loadProducts()
    }
})();