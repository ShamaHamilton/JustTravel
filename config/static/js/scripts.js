// для маленьких экранов
var navBar = document.getElementById("navBar");
function togglebtn() {
    navBar.classList.toggle("hidemenu");
}

// выделение активного окна
$('.nav-links li a').each(function () {
    let location = window.location.protocol + '//' + window.location.host + window.location.pathname;
    let link = this.href;
    if (location == link) {
        $(this).addClass('active');
    }
});

// выделение активного окна в личном кабинете
$('.header-links li a').each(function () {
    let location = window.location.protocol + '//' + window.location.host + window.location.pathname;
    let link = this.href;
    if (location == link) {
        $(this).addClass('header-active');
    }
});

$("#id_phone").mask("+7 (999) 999-99-99")

// Add star rating
const rating = document.querySelector('form[name=rating]');

rating.addEventListener("change", function (e) {
    // Получаем данные из формы
    let data = new FormData(this);
    fetch(`${this.action}`, {
        method: 'POST',
        body: data
    })
    // .then(response => alert("Оценка установлена"))
    // .catch(error => alert("Ошибка"))
});


// modal
var modal = document.getElementById("myModal");
var btn = document.getElementById("modalBtn");
var span = document.getElementsByClassName("closeBtn")[0];
btn.onclick = function () {
    modal.style.display = "block";
}
span.onclick = function () {
    modal.style.display = "none";
}
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}