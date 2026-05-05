(function () {
    "use strict";

    function scrollToEstimateResult() {
        var el = document.getElementById("estimate-result");
        if (!el) {
            return;
        }
        requestAnimationFrame(function () {
            el.scrollIntoView({ behavior: "smooth", block: "start" });
        });
    }

    function bindPrintEstimateFormSubmit() {
        var form = document.getElementById("print-estimate-form");
        if (!form) {
            return;
        }
        form.addEventListener("submit", function () {
            var btn = form.querySelector(
                'button[type="submit"], input[type="submit"]'
            );
            if (!btn) {
                return;
            }
            btn.disabled = true;
            btn.dataset.originalHtml = btn.innerHTML;
            btn.innerHTML =
                '<i class="fas fa-spinner fa-spin mr-1"></i> Calculando…';
            btn.classList.add("disabled");
        });
    }

    function init() {
        scrollToEstimateResult();
        bindPrintEstimateFormSubmit();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
