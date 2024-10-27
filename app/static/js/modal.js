function openModal(url){
    $('.address__form-add').attr('action',`${url}`)
    $('.modal').css('display','flex')
}

function closeModal(){
    $('.modal').css('display','none')
    $('.modal').find('input[name]').val('')
    $('.modal').find('select').val('0')
}