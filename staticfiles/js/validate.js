_$_$=document.querySelectorAll.bind(document)
_$=document.querySelector.bind(document)


function Validator(options){
    let selectorRule={}
    var formElement=_$(options.form)
    
    var rules=options.rules
    function addValidate(element,error){
        element.classList.add('input__error')
        let parent=element.parentElement
        let html=`<p class="validation">${error}</p>`
        let node=document.createElement('div')
        node.innerHTML=html
        parent.appendChild(node)
    }
    function removeValidate(element){
        if(element.classList.contains('input__error')){
            element.classList.remove('input__error')
            let parent=element.parentElement
            parent.removeChild(parent.lastElementChild)
        }
    }
    function handelValidate(element,tests){
        var errorMessage=null
        if(element!=null){
            for(let test of tests){
                let value=element.value
                errorMessage=test(value)
                if(errorMessage) break
            }
            if(errorMessage){
                removeValidate(element)
                addValidate(element,errorMessage)
            }
        }
        return errorMessage

    }
    Array.from(rules).forEach(rule=>{
        if(Array.isArray(selectorRule[rule.selector])){
            selectorRule[rule.selector].push(rule.test)
        }else{
            selectorRule[rule.selector]=[rule.test]
        }

    })
    for (let [key,tests] of Object.entries(selectorRule)){
        let element = formElement.querySelector(key)
        if(element!=null){
            element.onblur=function(){
                handelValidate(element,tests)
            }
            element.oninput=function(){
                removeValidate(this)
            }
        }

    }
    formElement.onsubmit=function(e){
        
        let sumitable=true
        for (let [key,tests] of Object.entries(selectorRule)){
            let element = formElement.querySelector(key)
            removeValidate(this)
            let error=handelValidate(element,tests)
            if(error){
                sumitable=false
            }
        }
        if(!sumitable){
            e.preventDefault()
        }

    }
    
}




Validator.isUsername =function (selector) {
    return{
        selector:selector,
        test: function(username){
            const hasValidLength = username.length >= 8;
            const hasNoSpecialChars = /^[a-zA-Z0-9]+$/.test(username);
            if (!hasValidLength) {
                return "Tên phải có ít nhất 8 ký tự.";
            }
            if (!hasNoSpecialChars) {
                return "Tên đăng nhập không được chứa ký tự đặc biệt.";
            }
            return null;
        }
    }
}

Validator.isEmail=function (selector) {
    return{
        selector:selector,
        test:function(email){
            const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
            if (!emailPattern.test(email)) {
                return "Địa chỉ email không hợp lệ.";
            }
            return null;
        }
    }
}

Validator.isPhone=function(selector){
    return{
        selector:selector,
        test:function (phone) {
            const phonePattern = /^[0-9]{10}$/;
        
            if (!phonePattern.test(phone)) {
                return "Số điện thoại phải có đúng 10 chữ số và chỉ được chứa các ký tự số.";
            }
        
            return null;
        }
    }
}

Validator.isRequired=function(selector){
    return{
        selector:selector,
        test:function (value){
            if (value.length>0){
                return null
            }
            return "Vui lòng nhập trường này."
        }
        
    }
}

Validator.isPassword=function(selector){
    return {
        selector:selector,
        test:function (password) {
            const lengthCriteria = /.{8,}/;
            const upperCaseCriteria = /[A-Z]/;
            const lowerCaseCriteria = /[a-z]/;
            const numberCriteria = /[0-9]/;
            const specialCharCriteria = /[!@#$%^&*(),.?":{}|<>]/;
        
            if (!lengthCriteria.test(password)) {
                return "Mật khẩu phải có ít nhất 8 ký tự.";
            }
            if (!upperCaseCriteria.test(password)) {
                return "Mật khẩu phải có ít nhất một chữ cái viết hoa.";
            }
            if (!lowerCaseCriteria.test(password)) {
                return "Mật khẩu phải có ít nhất một chữ cái viết thường.";
            }
            if (!numberCriteria.test(password)) {
                return "Mật khẩu phải có ít nhất một chữ số.";
            }
            if (!specialCharCriteria.test(password)) {
                return "Mật khẩu phải có ít nhất một ký tự đặc biệt.";
            }
        
            return null;
        }
    }
}

Validator.isConfirmPassword=function(selector,password){
    return{
        selector:selector,
        test: function(confirmPassword) {
            if (password() !== confirmPassword) {
                return "Xác nhận mật khẩu không khớp.";
            }
            return null;
        }
    }
}

Validator.isSelected=function(selector){
    return{
        selector:selector,
        test:function(option){
            return option==='0' ? 'Vui lòng chọn trường này': null
        }

    }
}



