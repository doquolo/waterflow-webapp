const populateUserList = () => {
    fetch(`/getAllUserData?sessionid=${sessionid}`)
    .then((res) => {
        return res.json();
    })
    .then((res) => {
        if (res.status === "error") {
            if (res.error === "expired") {
                alert("Phiên đã hết hạn, vui lòng đăng nhập lại!");
            } else if (res.error == "invalid") {
                alert("Phiên không hợp lệ, vui lòng đăng nhập lại!");
            }
        }
        else {
            userlist = document.querySelector(".userList")
            let template = "";
            for (let i in res) {
                devicelist = ""
                for (let j in res[i].devices) {
                    devicelist += `<div class="device">${res[i].devices[j]}<div class="w3-button action" onclick="unlink('${res[i].username}', '${res[i].devices[j]}')">Huỷ liên kết</div></div>
                            `;
                }
                template += `<div class="user">
                    <div class="username-box">
                        <p>Tên người dùng: </p>
                        <p class="username">${res[i].username}</p>
                        <div class="w3-button action" onclick="delUser('${res[i].username}')">Xoá</div>
                    </div>
                    <div class="device-list">
                        <div class="device-action">
                            <p>Các thiết bị đang liên kết: </p>
                            <div class="w3-button action" onclick="newLink('${res[i].username}')">Liên kết mới</div>
                        </div>
                        <div class="devices">${devicelist}</div>
                    </div>
                </div>`
            }
            userlist.innerHTML = `        <div class="userList">
                <div class="w3-button action" style="margin: 1rem 0rem;" onclick="createNewUser()">Tạo người dùng mới</div>
                ${template}
                </div>`;
        }
    })
}

const delUser = (username) => {
    // TODO: delete user from database
    fetch(`/delUser?username=${username}`)
        .then((res) => {return res.json()})
        .then((res) => {
            if (res.state == "done") alert(`Đã xoá người dùng ${username}`);
            else alert(`Hệ thống lỗi: ${res.error}`);
            // repopulate the list
            populateUserList();
        })
}

const newLink = (username) => {
    let deviceid = prompt("Nhập ID thiết bị muốn liên kết: ");
    fetch(`/newLink?username=${username}&deviceid=${deviceid}`)
        .then((res) => {return res.json()})
        .then((res) => {
            if (res.state == "done") alert(`Đã thêm liên kết!`);
            else alert(`Hệ thống lỗi: ${res.error}`);
            // repopulate the list
            populateUserList();
        })
}

const unlink = (username, id) => {
    fetch(`/unlink?username=${username}&deviceid=${id}`)
        .then((res) => {return res.json()})
        .then((res) => {
            if (res.state == "done") alert(`Đã huỷ liên kết!`);
            else alert(`Hệ thống lỗi: ${res.error}`);
            // repopulate the list
            populateUserList();
        })
}

const createNewUser = () => {
    const username = prompt("Nhập tên đăng nhập của người dùng mới: ");
    const password = prompt("Nhập mật khẩu của người dùng mới: ");
    argon2.hash({ pass: password, salt: "somesalt"})
    .then(h => {
        console.log(h.encoded);
        fetch(`/registerNewUser`, {
            method: "POST",
            body: JSON.stringify({
              user: username,
              hash: h.encoded,
            })
        })
        .then((res) => {return res.json()})
        .then((res) => {
            if (res.state == "done") alert(`Đã thêm tài khoản mới!`);
            else alert(`Hệ thống lỗi: ${res.error}`);
            // repopulate the list
            populateUserList();
        })
    })
    .catch(e => alert(e.message, e.code))
}

document.addEventListener("DOMContentLoaded", () => {
    populateUserList();
})