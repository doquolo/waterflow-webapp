const checker = () => {
    fetch("/getAdminData", {
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
        } else if (data.state === "found") {
          sessionid = data.sessionid;
          return true;
        } else {
          alert(`Hệ thống lỗi: ${data.e}`);
        }
      })
      .then((state) => {
        if (state) {
            alert("Đăng nhập thành công!");
            const welcome_text = document.querySelector("#welcome_text");

            welcome_text.textContent = `Xin chào quản trị viên, ${username}`;
        }
      });
  };

// login
let username = prompt("Username");
let password = prompt("Password");

let sessionid = "";

checker();