// Function to toggle the sidebar visibility
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar'); // Sidebar element
    const navbar = document.querySelector('.navbar'); // Navbar element
    const mainContent = document.querySelector('.main-content'); // Main content element

    // Toggle the 'collapsed' class on the sidebar
    sidebar.classList.toggle('collapsed');
    navbar.classList.toggle('collapsed'); // Adjust navbar when sidebar collapses
    mainContent.classList.toggle('collapsed'); // Adjust main content when sidebar collapses
}

// Add event listener for the toggle button
document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.querySelector('.toggle-btn');
    toggleButton.addEventListener('click', toggleSidebar); // Call the toggle function when clicked
});
