function toggleSidebar() {
    const sidebar = document.getElementById('sidebar'); // Sidebar element
    const navbar = document.querySelector('.navbar'); // Navbar element
    const mainContent = document.querySelector('.main-content'); // Main content element
    const menu = document.querySelector('.menu');

    // Toggle the 'collapsed' class on the sidebar
    sidebar.classList.toggle('collapsed');

    // Adjust layout dynamically based on the sidebar state
    if (sidebar.classList.contains('collapsed')) {
        navbar.classList.add('collapsed'); // Adjust navbar position
        mainContent.classList.add('collapsed'); // Adjust main content
        menu.classList.add("hide")
        if (menu) {
            menu.style.display = "none"; // Debugging with inline style
        }
    } else {
        navbar.classList.remove('collapsed'); // Restore navbar position
        mainContent.classList.remove('collapsed'); // Restore main content
         // Restore menu visibility
         if (menu) {
            menu.style.display = ""; // Restore default style
        }
    }
}

// Add event listener for the toggle button
document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.querySelector('.toggle-btn');
    toggleButton.addEventListener('click', toggleSidebar);
});