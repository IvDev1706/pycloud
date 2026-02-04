//seleccionar elementos
const window_layer = document.getElementById("window-cont");
const newdir_btn = document.getElementById("new-dir");
const dir_box = document.getElementById("dir-box");

//vincular escuchas
newdir_btn.addEventListener("click",(e)=>{
    //mostrar caja
    dir_box.style.display = "flex";
    //mostrar capa
    window_layer.style.display = "block";
});