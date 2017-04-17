var cur_count;
var count = 60;
var InterValObj;
var phone;

function send_message(url, phone_num=null) {
    if (phone_num) {
        phone = phone_num;
    }
    else {
        phone = document.getElementById("phone").value;
    }
    if (phone) {
        cur_count = count;
        document.getElementById("code").setAttribute("disabled", "true");
        document.getElementById("code").textContent = "等待" + cur_count + "s";

        InterValObj = window.setInterval(set_remain_time, 1000);
        loadXMLDoc(url);
    }
}

function set_remain_time() {
    if (cur_count == 0) {
        window.clearInterval(InterValObj);
        document.getElementById("code").removeAttribute("disabled");
        document.getElementById("code").textContent = "获取验证码";
    } else {
        cur_count--;
        document.getElementById("code").textContent = "等待" + cur_count + "s";
    }
}

function loadXMLDoc(url) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", url + "?phone=" + phone, true);
    xmlhttp.send(null);
}

$(".submit-order").on("click", function() {
    var self = this;
    var schedule_id = $(self).children("input").val();
    alert("ss");
    $.ajax({
        url: "submit-order",
        data: {
            "schedule_id": schedule_id
        },
        type: "GET"
    })
});

$("table").on("click", ".cancel-order", function() {
    var self = this
    var order_id = self.id;
    $.ajax({
        url: "cancel-order",
        data: {
            "order_id": order_id
        },
        type: "GET"
    })
    .done(function() {
        $(self).parent().remove();
    })
});

$("table").on("click", ".kyy", function() {
    var self = this
    var week_time = $(self).children("input").val();
    $.ajax({
        url: "/auth/show-doctor",
        data: {
            "week_time": week_time
        },
        type: "GET"
    })
    .done(function (data) {
        $(".doctor").html(data)
    })
});

$("#addr").distpicker({
    autoSelect: false
});
$("#change-addr").distpicker();
