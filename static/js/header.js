//Nav bar
function loadHeader() {
    fetch('header.html')
                .then(response => response.text())
                .then(data => {
                    document.getElementById('header-placeholder').innerHTML = data;
                });
        }
 document.addEventListener('DOMContentLoaded', loadHeader);

