const hamb = document.getElementById('hamb');
const sidebar = document.getElementById('sidebar');
const main = document.getElementById('main');
const profile = document.getElementById('profile');
const profileMenu = document.getElementById('profileMenu');

function toggleSidebar(){
  if(sidebar.classList.contains('hidden')){
    sidebar.classList.remove('hidden');
    main.classList.remove('full');
  } else {
    sidebar.classList.add('hidden');
    main.classList.add('full');
  }
}

function toggleProfileMenu() {
  if (profileMenu.classList.contains('active')) {
    profileMenu.classList.remove('active');
  } else {
    profileMenu.classList.add('active');
  }
}

hamb.addEventListener('click', toggleSidebar);

// Toggle profile menu on click
profile.addEventListener('click', function(e) {
  // Prevent the click from immediately closing the menu
  e.stopPropagation();
  toggleProfileMenu();
});

// Close profile menu when clicking outside
document.addEventListener('click', function(e) {
  if (!profile.contains(e.target)) {
    profileMenu.classList.remove('active');
  }
});

// Keep menu open when hovering over it
profileMenu.addEventListener('mouseenter', function() {
  profileMenu.classList.add('active');
});

profileMenu.addEventListener('mouseleave', function() {
  // Don't close immediately on mouse leave to allow clicking
  setTimeout(() => {
    if (!profileMenu.matches(':hover') && !profile.matches(':hover')) {
      profileMenu.classList.remove('active');
    }
  }, 100);
});

window.addEventListener('resize', ()=>{
  if(window.innerWidth>980){
    sidebar.classList.remove('hidden');
    main.classList.remove('full');
  } else {
    sidebar.classList.add('hidden');
    main.classList.add('full');
  }
});

