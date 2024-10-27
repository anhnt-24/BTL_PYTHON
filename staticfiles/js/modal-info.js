
function closeInfoModal(){
    $('.modal__info').removeClass('modal__info-open')
    setTimeout(function(){
        $('body').children('.modal__info').remove()
    },300)
}
function handleDataInforModal(data){
	data()
    closeInfoModal()
}
function renderInforModal(info,type,data){

    let html=`<div class="modal__info">
            <p class="modal__info-header">
            Thông báo  
            </p>
            <p class="modal__info-body">
               ${info}
            </p>
            <div class="modal__info-btn-container">
                <button class="modal__info-btn btn_hover modal__info-btn-ok"  onclick="closeInfoModal()">Ok</button>
            </div>
        </div>`
    if(type){
        html=`<div class="modal__info">
            <p class="modal__info-header">
            Thông báo  
            </p>
            <p class="modal__info-body">
               ${info}
            </p>
            <div class="modal__info-btn-container">
                <button class="modal__info-btn btn_hover modal__info-btn-approve" onclick="handleDataInforModal(${data})">Xác nhận</button>
                <button class="modal__info-btn btn_hover modal__info-btn-cancel" onclick="closeInfoModal()">Hủy</button>
            </div>
        </div>`
    }
    $('body').append(html)
    setTimeout(function(){
        $('.modal__info').addClass('modal__info-open')
    },10)

}

function renderModalSuccess(img,noti){
    var html =`
        <div class="modal__success">
        <img src=${img}  height="100">
        <p class=" modal__success-header">${noti}</p>
        </div> 
    `
    setTimeout(function(){
            $('body').children(".modal__success").last().remove()
    },3000)
    $('body').append(html)
   
}