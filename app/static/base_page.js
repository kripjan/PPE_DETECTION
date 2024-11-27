const sidebar = document.querySelector(".sidebar");
const sidebarToggler = document.querySelector(".sidebar-toggler");
const menuToggler = document.querySelector(".menu-toggler");

const collapsedSidebarHeight = "56px";

// Toggler sidebar's collapsed state
sidebarToggler.addEventListener("click", () => {
    sidebar.classList.toggle("collapsed");
});

const toggleMenu = (isMenuActive)=>{
    sidebar.style.height = isMenuActive ? `${sidebar.scrollHeight}px` : collapsedSidebarHeight;
    menuToggler.querySelector("span").innerText = isMenuActive ? "close" : "menu";
}

//Toggle menu-active class and adjust height
menuToggler.addEventListener("click", () => {
    toggleMenu(sidebar.classList.toggle("menu-active"));
});

window.addEventListener("resize", () => {
    if (window.innerWidth >= 1024) {
        sidebar.computedStyleMap.height = fullSidebarHeight;
    } else {
        sidebar.classList.remove("collapsed");
        sidebar.computedStyleMap.height = "auto";
        toggleMenu(sidebar.classList.contains("menu-active"))
    }
})