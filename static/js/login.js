const checker = () => {
    fetch("/getUserData", {
      method: "POST",
      body: JSON.stringify({
        user: username,
        password: password,
      }),
    })
      .then((request) => {
        console.log(request.status);
        return request.json();
      })
      .then((request) => {
        const data = request;
        if (data.state === "authenticate") {
          alert("Tên đăng nhập hoặc mật khẩu sai!");
          username = prompt("Nhập lại username:");
          password = prompt("Nhập lại password");
          checker();
        } else if (data.state === "notfound") {
          state = true;
          return true;
        } else {
          state = true;
          isMachineAvail = true;
          data_json = request;
          return true;
        }
      })
      .then((repeat) => {
        if (repeat) {
          console.log(data, state, isMachineAvail);
          if (state && !isMachineAvail) {
            alert("Không có thiết bị nào liên kết với tài khoản của bạn!");
          } else if (state) {
            alert("Đăng nhập thành công!");
            const welcome_text = document.querySelector("#welcome_text");
            const dropdown = document.querySelector("#devices");

            welcome_text.textContent = `Xin chào, ${username}`;
            for (let i in data_json.data.machines) {
              dropdown.innerHTML += 
                `<option value="${data_json.data.machines[i]}">${data_json.data.machines[i]}</option>`;
            }
          }
        }
      });
  };

// login
let username = prompt("Username");
let password = prompt("Password");

let state = false;
let isMachineAvail = false;
let data_json = null;

checker();