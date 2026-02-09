//capa y cajas
const window_layer = document.getElementById("window-cont");
const dir_box = document.getElementById("dir-box");
const file_box = document.getElementById("file-box");
const rmdir_box = document.getElementById("drop-dir-box");

//botones
const newdir_btn = document.getElementById("new-dir");
const dir_close = document.getElementById("dir-close");
const file_btn = document.getElementById("upload-file");
const file_close = document.getElementById("file-close");
const rmdir_btn = document.getElementById("rm-dir");
const drop_close = document.getElementById("drop-close");

//funcion para ocultar la ventana
function showWindow(cont, box){
    //mostrar la caja
    box.style.display = "flex";
    //mostrar capa
    cont.style.display = "block";
}

//funcion para mostrar la ventana
function hideWindow(cont, box){
    //mostrar la caja
    box.style.display = "none";
    //mostrar capa
    cont.style.display = "none";
}

//vincular escuchas
newdir_btn.addEventListener("click",(e)=>{
    showWindow(window_layer,dir_box);
});

file_btn.addEventListener("click",(e)=>{
    showWindow(window_layer,file_box);
});

rmdir_btn.addEventListener("click",(e)=>{
    showWindow(window_layer,rmdir_box);
});

dir_close.addEventListener("click",(e)=>{
    hideWindow(window_layer,dir_box);
});

file_close.addEventListener("click",(e)=>{
    hideWindow(window_layer,file_box);
});

drop_close.addEventListener("click",(e)=>{
    hideWindow(window_layer,rmdir_box);
});