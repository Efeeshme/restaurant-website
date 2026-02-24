(() => {
  "use strict";

  // === CONFIG ===
  const CONFIG = {
    headerOffset: 16,
    dragScrollMultiplier: 1.5,
    modalClass: "no-scroll"
  };

  // === DOM CACHE ===
  const DOM = {
    catButtons: document.querySelectorAll(".cat-btn"),
    panels: document.querySelectorAll(".menu__panel[data-panel]"),
    modal: document.getElementById("modal"),
    modalImg: document.getElementById("m-img"),
    modalTitle: document.getElementById("m-title"),
    modalPrice: document.getElementById("m-price"),
    modalDesc: document.getElementById("m-desc"),
    modalMedia: null,
    modalClose: null,
    header: document.querySelector(".header"),
    nav: document.querySelector(".nav"),
    navLinks: document.querySelectorAll('.nav a[href^="#"]')
  };

  // Initialize modal elements if modal exists
  if (DOM.modal) {
    DOM.modalMedia = DOM.modal.querySelector(".modal__media");
    DOM.modalClose = DOM.modal.querySelector(".modal__close");
  }

  // === CATEGORY TABS ===
  const CategoryTabs = {
    init() {
      if (!DOM.catButtons.length) return;

      DOM.catButtons.forEach(btn => {
        btn.addEventListener("click", () => this.showPanel(btn.dataset.cat));
      });
    },

    showPanel(id) {
      // Update buttons
      DOM.catButtons.forEach(btn => {
        btn.setAttribute("aria-selected", btn.dataset.cat === id);
      });

      // Update panels
      DOM.panels.forEach(panel => {
        panel.hidden = panel.dataset.panel !== id;
      });
    }
  };

  // === MODAL ===
  const Modal = {
    init() {
      if (!DOM.modal) return;

      // Click handlers
      document.addEventListener("click", this.handleClick.bind(this));

      // Keyboard handlers
      document.addEventListener("keydown", this.handleKeydown.bind(this));
    },

    handleClick(e) {
      // Open modal
      const cardBtn = e.target.closest(".card__btn");
      if (cardBtn) {
        e.preventDefault();
        this.open({
          name: cardBtn.dataset.name,
          price: cardBtn.dataset.price,
          desc: cardBtn.dataset.desc,
          img: cardBtn.dataset.img
        });
        return;
      }

      // Close modal
      if (e.target.closest("[data-close]") || e.target === DOM.modal?.querySelector(".modal__backdrop")) {
        e.preventDefault();
        this.close();
      }
    },

    handleKeydown(e) {
      if (e.key === "Escape" && DOM.modal?.getAttribute("aria-hidden") === "false") {
        this.close();
      }
    },

    open(data) {
      if (!DOM.modal) return;

      // Set content
      DOM.modalTitle.textContent = data.name || "";
      DOM.modalPrice.textContent = data.price ? `${data.price} ₼` : "";
      DOM.modalDesc.textContent = data.desc || "—";

      // Handle image
      if (data.img) {
        DOM.modalImg.src = data.img;
        DOM.modalImg.alt = data.name || "";
        if (DOM.modalMedia) DOM.modalMedia.style.display = "block";
      } else {
        DOM.modalImg.removeAttribute("src");
        DOM.modalImg.alt = "";
        if (DOM.modalMedia) DOM.modalMedia.style.display = "none";
      }

      // Show modal
      DOM.modal.setAttribute("aria-hidden", "false");
      document.body.classList.add(CONFIG.modalClass);

      // Focus close button
      DOM.modalClose?.focus();
    },

    close() {
      if (!DOM.modal) return;

      DOM.modal.setAttribute("aria-hidden", "true");
      document.body.classList.remove(CONFIG.modalClass);
    }
  };

  // === SMOOTH SCROLL ===
  const SmoothScroll = {
    init() {
      if (!DOM.navLinks.length) return;

      DOM.navLinks.forEach(link => {
        link.addEventListener("click", this.handleClick.bind(this));
      });
    },

    handleClick(e) {
      e.preventDefault();
      const target = document.querySelector(e.currentTarget.getAttribute("href"));
      if (!target) return;

      const headerHeight = DOM.header?.offsetHeight || 0;
      const targetPosition = target.offsetTop - headerHeight - CONFIG.headerOffset;

      window.scrollTo({
        top: targetPosition,
        behavior: "smooth"
      });
    }
  };

  // === DRAG SCROLL (Optional Enhancement) ===
  const DragScroll = {
    state: {
      isDown: false,
      startX: 0,
      scrollLeft: 0
    },

    init() {
      if (!DOM.nav) return;

      DOM.nav.addEventListener("mousedown", this.onMouseDown.bind(this));
      DOM.nav.addEventListener("mouseleave", this.onMouseLeave.bind(this));
      DOM.nav.addEventListener("mouseup", this.onMouseUp.bind(this));
      DOM.nav.addEventListener("mousemove", this.onMouseMove.bind(this));
    },

    onMouseDown(e) {
      this.state.isDown = true;
      this.state.startX = e.pageX - DOM.nav.offsetLeft;
      this.state.scrollLeft = DOM.nav.scrollLeft;
    },

    onMouseLeave() {
      this.state.isDown = false;
    },

    onMouseUp() {
      this.state.isDown = false;
    },

    onMouseMove(e) {
      if (!this.state.isDown) return;
      e.preventDefault();

      const x = e.pageX - DOM.nav.offsetLeft;
      const walk = (x - this.state.startX) * CONFIG.dragScrollMultiplier;
      DOM.nav.scrollLeft = this.state.scrollLeft - walk;
    }
  };

  // === KEYBOARD NAVIGATION ===
  const KeyboardNav = {
    init() {
      document.addEventListener("keydown", this.onKeyDown.bind(this));
      document.addEventListener("mousedown", this.onMouseDown.bind(this));
    },

    onKeyDown(e) {
      if (e.key === "Tab") {
        document.body.classList.add("keyboard-nav");
      }
    },

    onMouseDown() {
      document.body.classList.remove("keyboard-nav");
    }
  };

  // === INITIALIZE ALL MODULES ===
  const init = () => {
    CategoryTabs.init();
    Modal.init();
    SmoothScroll.init();
    DragScroll.init();
    KeyboardNav.init();
  };

  // Start when DOM is ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
