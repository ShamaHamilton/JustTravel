
// flatpickr на главной странице
config = {
    "locale": "ru",
    // dateFormat: "Y-m-d",
    dateFormat: "d-m-Y",
    minDate: "today",
    disableMobile: "true",
}
datepickr = flatpickr("input[type=date]", config);

// flatpickr в бронировании жилья
// Прибытие-настройки
const value1 = JSON.parse(document.getElementById('value1').textContent);
config1 = {
    "locale": "ru",
    dateFormat: "d.m.Y",
    minDate: "today",
    disable: value1,
    disableMobile: "true",
}
// Выезд-настройки
const value2 = JSON.parse(document.getElementById('value2').textContent);
config2 = {
    "locale": "ru",
    dateFormat: "d.m.Y",
    minDate: "today",
    disable: value2,
    disableMobile: "true",
}
startPicker = flatpickr("input[type=date_in]", config1);
endPicker = flatpickr("input[type=date_out]", config2);