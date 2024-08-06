//Nav bar
function loadHeader() {
    fetch('header.html')
                .then(response => response.text())
                .then(data => {
                    document.getElementById('header-placeholder').innerHTML = data;
                });
        }
 document.addEventListener('DOMContentLoaded', loadHeader);


 // JavaScript for profile modal and file upload
 document.addEventListener("DOMContentLoaded", function() {
    var modal = document.getElementById("profileModal");
    var btn = document.getElementById("view-profile");
    var span = document.getElementsByClassName("close")[0];
    var profilePhoto = document.getElementById("profilePhoto");
    var modalProfilePhoto = document.getElementById("profilePhoto");
    var fileInput = document.getElementById("profilePhotoInput");

    btn.onclick = function() {
        modal.style.display = "block";
    }

    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    modalProfilePhoto.onclick = function() {
        fileInput.click();
    }

    fileInput.onchange = function(event) {
        var file = event.target.files[0];
        var formData = new FormData();
        formData.append('profile_photo', file);

        fetch('/update_profile', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                profilePhoto.src = data.photo_url;
                modalProfilePhoto.src = data.photo_url;
            } else {
                alert('Failed to upload photo: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});
