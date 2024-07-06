function tinhTienNuoc(luongNuoc) {
    var muc1 = 5.973; // đồng/m3 cho 10m3 đầu tiên sử dụng
    var muc2 = 7.052; // đồng/m3 cho mức sử dụng từ 10 - 20m3
    var muc3 = 8.669; // đồng/m3 cho mức sử dụng từ 20 - 30m3
    var muc4 = 15.929; // đồng/m3 cho mức sử dụng từ 30m3 trở lên

    var tienNuoc = 0;

    if (luongNuoc <= 10) {
      tienNuoc = luongNuoc * muc1;
    } else if (luongNuoc <= 20) {
      tienNuoc = 10 * muc1 + (luongNuoc - 10) * muc2;
    } else if (luongNuoc <= 30) {
      tienNuoc = 10 * muc1 + 10 * muc2 + (luongNuoc - 20) * muc3;
    } else {
      tienNuoc = 10 * muc1 + 10 * muc2 + 10 * muc3 + (luongNuoc - 30) * muc4;
    }

    return tienNuoc;
  }

  const getData = (date, device_id) => {
    console.log(date);
    fetch(`/getdata?date=${date}&deviceid=${device_id}`)
      .then((data) => {
        return data.json();
      })
      .then((data) => {
        if (data.error === "true") {
          alert("Không tìm thấy dữ liệu cho ngày này!");
          return 0;
        }
        const xValues = [];
        const y1Values = [];
        const y2Values = [];

        for (let i in data) {
          var date = new Date(i * 1000); // sec to ms
          xValues.push(`${date.getHours()}:${date.getMinutes()}`);
          y1Values.push(Number(data[i]["waterFlowed"]) / 1000);
          y2Values.push(Number(data[i]["waterSpeed"]) / 1000);
        }
        // fill in info
        const waterused = y1Values.at(-1);
        document.querySelector(
          "#waterused"
        ).textContent = `Số nước tạm tính trong ngày: ${waterused} (m3)`;

        document.querySelector(
          "#estimated"
        ).textContent = `Tiền nước tạm tính trong ngày: ${tinhTienNuoc(
          waterused
        )} (đồng)`;
        // make chart
        new Chart("myChart", {
          type: "line",
          data: {
            labels: xValues,
            datasets: [
              {
                fill: false,
                lineTension: 0,
                backgroundColor: "rgba(0,0,255,1.0)",
                borderColor: "rgba(0,0,255,0.1)",
                data: y1Values,
                label: "Số nước (m3)",
                color: "rgba(0,0,255,1.0)",
              },
              {
                fill: false,
                lineTension: 0,
                backgroundColor: "rgba(0,255,0,1.0)",
                borderColor: "rgba(0,0,255,0.1)",
                data: y2Values,
                label: "Tốc độ dòng chảy (m3/phút)",
                color: "rgba(0,255,0,1.0)",
              },
            ],
          },
          options: {
            elements: {
              point: {
                radius: 6,
                hoverRadius: 5, // ex.: to make it bigger when user hovers put larger number than radius.
              },
              line: {
                borderWidth: 5,
              },
            },
            legend: { display: true },
            scales: {
              yAxes: [{ ticks: {} }],
            },
          },
        });
      });
  };

  function formatDate(date) {
    // Extract day, month, and year from the date object
    var day = date.getDate();
    var month = date.getMonth() + 1; // Month is zero-based, so we add 1
    var year = date.getFullYear();

    // Pad day and month with leading zeros if needed
    if (day < 10) {
      day = "0" + day;
    }
    if (month < 10) {
      month = "0" + month;
    }

    // Concatenate day, month, and year in the desired format
    var formattedDate = "" + day + month + year;

    return formattedDate;
  }

  const handleDatepicker = () => {
    numdate = document.querySelector("#numdate");
    nummonth = document.querySelector("#nummonth");
    numyear = document.querySelector("#numyear");
    let device = document.querySelector("#devices").value;
    if (device == "-") alert("Chọn thiết bị để xem dữ liệu!");
    else if (numyear.value == "" || nummonth.value == "" || numdate.value == "")
      alert("Chọn ngày trước khi lấy dữ liệu!");
    else {

      const date = new Date(`${Number(numyear.value)},${Number(nummonth.value)},${Number(numdate.value)}`);
      getData(formatDate(date), device);
    }
  };