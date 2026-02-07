//seleccionar elementos
const window_layer = document.getElementById("window-cont");
const newdir_btn = document.getElementById("new-dir");
const dir_box = document.getElementById("dir-box");
const file_btn = document.getElementById("upload-file");
const file_box = document.getElementById("file-box");
const rmdir_btn = document.getElementById("rm-dir");
const rmdir_box = document.getElementById("drop-dir-box");

//vincular escuchas
newdir_btn.addEventListener("click",(e)=>{
    //mostrar caja
    dir_box.style.display = "flex";
    //mostrar capa
    window_layer.style.display = "block";
});

file_btn.addEventListener("click",(e)=>{
    //mostrar caja
    file_box.style.display = "flex";
    //mostrar capa
    window_layer.style.display = "block";
});

rmdir_btn.addEventListener("click",(e)=>{
    //mostrar caja
    rmdir_box.style.display = "flex";
    //mostrar capa
    window_layer.style.display = "block";
});