//DANES
function addDateAndSubmit() {
    var currentDate = new Date();
    var day = currentDate.getDate();
    var month = currentDate.getMonth() + 1; // getMonth() returns 0-11 so we need to add 1
    var year = currentDate.getFullYear();
    var dateString = day + "." + month + "." + year;
    document.getElementById("id_od").value = dateString;
}
//Jutri
function JutriAndSubmit() {
    var currentDate = new Date();
    var Jutri = new Date(currentDate);
    Jutri.setDate(Jutri.getDate() + 1)
    var day = Jutri.getDate();
    var month = Jutri.getMonth() + 1; // getMonth() returns 0-11 so we need to add 1
    var year = Jutri.getFullYear();
    var dateString = day + "." + month + "." + year;
    document.getElementById("id_od").value = dateString;
   
}




// + 1 dan
function Plus1DanInSubmit() {
    var dateField = document.getElementById('id_od');
    var DatumDO = document.getElementById('id_do');
    var dateArray = dateField.value.split('.');
    var day = parseInt(dateArray[0]);
    var month = parseInt(dateArray[1]) - 1;
    var year = parseInt(dateArray[2]);
    var currentDate = new Date(year, month, day);
    var newDate = new Date(currentDate.getTime() + 1 * 24 * 60 * 60 * 1000);
    day = newDate.getDate();
    month = newDate.getMonth() + 1;
    year = newDate.getFullYear();
    DatumDO.value = day + "." + month + "." + year;
   
}
function Plus2DanInSubmit() {
    var dateField = document.getElementById('id_od');
    var DatumDO = document.getElementById('id_do');
    var dateArray = dateField.value.split('.');
    var day = parseInt(dateArray[0]);
    var month = parseInt(dateArray[1]) - 1;
    var year = parseInt(dateArray[2]);
    var currentDate = new Date(year, month, day);
    var newDate = new Date(currentDate.getTime() + 2 * 24 * 60 * 60 * 1000);
    day = newDate.getDate();
    month = newDate.getMonth() + 1;
    year = newDate.getFullYear();
    DatumDO.value = day + "." + month + "." + year;
   
}

function Plus3DanInSubmit() {
    var dateField = document.getElementById('id_od');
    var DatumDO = document.getElementById('id_do');
    var dateArray = dateField.value.split('.');
    var day = parseInt(dateArray[0]);
    var month = parseInt(dateArray[1]) - 1;
    var year = parseInt(dateArray[2]);
    var currentDate = new Date(year, month, day);
    var newDate = new Date(currentDate.getTime() + 3 * 24 * 60 * 60 * 1000);
    day = newDate.getDate();
    month = newDate.getMonth() + 1;
    year = newDate.getFullYear();
    DatumDO.value = day + "." + month + "." + year;
   
}

function Plus4DanInSubmit() {
    var dateField = document.getElementById('id_od');
    var DatumDO = document.getElementById('id_do');
    var dateArray = dateField.value.split('.');
    var day = parseInt(dateArray[0]);
    var month = parseInt(dateArray[1]) - 1;
    var year = parseInt(dateArray[2]);
    var currentDate = new Date(year, month, day);
    var newDate = new Date(currentDate.getTime() + 4 * 24 * 60 * 60 * 1000);
    day = newDate.getDate();
    month = newDate.getMonth() + 1;
    year = newDate.getFullYear();
    DatumDO.value = day + "." + month + "." + year;
   
}

function Plus5DanInSubmit() {
    var dateField = document.getElementById('id_od');
    var DatumDO = document.getElementById('id_do');
    var dateArray = dateField.value.split('.');
    var day = parseInt(dateArray[0]);
    var month = parseInt(dateArray[1]) - 1;
    var year = parseInt(dateArray[2]);
    var currentDate = new Date(year, month, day);
    var newDate = new Date(currentDate.getTime() + 5 * 24 * 60 * 60 * 1000);
    day = newDate.getDate();
    month = newDate.getMonth() + 1;
    year = newDate.getFullYear();
    DatumDO.value = day + "." + month + "." + year;
   
}

function Plus6DanInSubmit() {
    var dateField = document.getElementById('id_od');
    var DatumDO = document.getElementById('id_do');
    var dateArray = dateField.value.split('.');
    var day = parseInt(dateArray[0]);
    var month = parseInt(dateArray[1]) - 1;
    var year = parseInt(dateArray[2]);
    var currentDate = new Date(year, month, day);
    var newDate = new Date(currentDate.getTime() + 6 * 24 * 60 * 60 * 1000);
    day = newDate.getDate();
    month = newDate.getMonth() + 1;
    year = newDate.getFullYear();
    DatumDO.value = day + "." + month + "." + year;
   
}

function Plus7DanInSubmit() {
    var dateField = document.getElementById('id_od');
    var DatumDO = document.getElementById('id_do');
    var dateArray = dateField.value.split('.');
    var day = parseInt(dateArray[0]);
    var month = parseInt(dateArray[1]) - 1;
    var year = parseInt(dateArray[2]);
    var currentDate = new Date(year, month, day);
    var newDate = new Date(currentDate.getTime() + 7 * 24 * 60 * 60 * 1000);
    day = newDate.getDate();
    month = newDate.getMonth() + 1;
    year = newDate.getFullYear();
    DatumDO.value = day + "." + month + "." + year;
   
}