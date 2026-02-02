//seleccionar elementos
const account_btn = document.getElementById("account");
const account_box = document.getElementById("account-box");
const account_layer = document.getElementById("window-cont");
const account_close = document.getElementById("account-close");

//vincular escuchas
account_btn.addEventListener("click",(e)=>{
    //mostrar caja
    account_box.style.display = "flex";
    //mostrar capa
    account_layer.style.display = "block";
});

account_close.addEventListener("click",(e)=>{
    //ocultar caja
    account_box.style.display = "none";
    //ocultar capa
    account_layer.style.display = "none";
});