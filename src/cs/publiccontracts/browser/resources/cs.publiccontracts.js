document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('ul.tabs').forEach(function (tabContainer) {
    let links = tabContainer.querySelectorAll('a');
    let activeLink =
      Array.from(links).find(
        (link) => link.getAttribute('href') === location.hash,
      ) || links[0];
    let activeContent = document.querySelector(activeLink.getAttribute('href'));

    activeLink.classList.add('active');

    links.forEach((link) => {
      let content = document.querySelector(link.getAttribute('href'));
      if (content !== activeContent) {
        content.style.display = 'none';
      }
    });

    tabContainer.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        e.preventDefault();

        // Remove active state and hide current content
        activeLink.classList.remove('active');
        activeContent.style.display = 'none';

        // Set new active link and content
        activeLink = e.target;
        activeContent = document.querySelector(activeLink.getAttribute('href'));

        activeLink.classList.add('active');
        activeContent.style.display = '';
      }
    });
  });
});
