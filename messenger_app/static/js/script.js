function toggleModal(modalId, state) {
    var modal = document.getElementById(modalId);
    modal.style.display = state;
}

function handleFormSubmit(event, callback) {
    event.preventDefault();
    var formData = new FormData(event.target);
    callback(formData);
}

function sendMessage(formData) {
    var csrfToken = getCookie('csrftoken');
    var recipient = formData.get('recipientUsername');
    var content = formData.get('messageText');

    var messageData = {
        sender: null,
        recipient: recipient,
        chat: null,
        content: content,
        timestamp: null
    };

    axios.post("/api/messages/", messageData, {
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then(function(response) {
        console.log('Сообщение успешно отправлено');
        toggleModal("sendMessageModal", "none");
    })
    .catch(function(error) {
        console.log(error);
    });
}

function createGroupChat(chatName) {
    var csrfToken = getCookie('csrftoken');

    var chatData = {
        "name": chatName,
        "participants": []
    };

    axios.post("/api/group-chats/", chatData, {
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        }
    })
    .then(function(response) {
        console.log('Group chat created successfully');
        window.location.href = "/chat/" + response.data.id;
    })
    .catch(function(error) {
        console.log('Failed to create group chat:', error);
        if (error.response) {
            console.log(error.response.data);
        }
    });
}

function uploadProfilePicture(formData) {
    var csrfToken = getCookie('csrftoken');

    axios.post("/api/profile/picture/", formData, {
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then(function(response) {
        var avatarElement = document.getElementById("avatar");
        avatarElement.src = response.data.avatar;
    })
    .catch(function(error) {
        console.log(error);
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.getElementById("openSendMessageModal").addEventListener("click", function() {
    toggleModal("sendMessageModal", "block");
});

document.getElementById("closeSendMessageModal").addEventListener("click", function() {
    toggleModal("sendMessageModal", "none");
});

document.getElementById("openCreateChatModal").addEventListener("click", function() {
    toggleModal("createChatModal", "block");
});

document.getElementById("closeCreateChatModal").addEventListener("click", function() {
    toggleModal("createChatModal", "none");
});

document.getElementById("sendMessageForm").addEventListener("submit", function(event) {
    handleFormSubmit(event, sendMessage);
});

document.getElementById("createChatForm").addEventListener("submit", function(event) {
    event.preventDefault();
    var chatName = document.getElementById("chatName").value;
    if (chatName) {
        createGroupChat(chatName);
    } else {
        console.log('Please enter a chat name');
    }
});

document.getElementById("uploadProfilePictureForm").addEventListener("submit", function(event) {
    handleFormSubmit(event, uploadProfilePicture);
});
