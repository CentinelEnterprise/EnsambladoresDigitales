$(document).ready(function() {
  $(".numeric").keydown(function (e) {
    if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
      (e.keyCode == 65 && e.ctrlKey === true) || 
      (e.keyCode >= 35 && e.keyCode <= 39)) {
       return;
    }
    if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
      e.preventDefault();
    }
  });
  $(".integer").keydown(function (e) {
    if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110]) !== -1 ||
      (e.keyCode == 65 && e.ctrlKey === true) || 
      (e.keyCode >= 35 && e.keyCode <= 39)) {
      return;
    }
    if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
      e.preventDefault();
    }
  });
  $(".characters").keydown(function (e) {
    if((e.keyCode<65 || e.keyCode>90) && (e.keyCode<97 || e.keyCode>122) && e.keyCode!=32 && e.keyCode!=46 && e.keyCode!=8 && e.keyCode!=192)  {
      e.preventDefault();
    }
  });
  $(".no-spaces").keydown(function (e) {
    if(e.keyCode==32)  {
      e.preventDefault();
    }
  });
});

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}
function formato_numeros(event){
  $(event.target).val(floatNumberWithCommas($(event.target).val()));
}
function formato_decimales(number){
  number = number.toString().replace(/\,/g,"");
  return parseFloat(Math.round(parseFloat(number) * 100) / 100).toFixed(2);
}

function floatNumberWithCommas(x) {
  //x = formato_decimales(x);
  x = x.toString().replace(/\,/g,"");
  var parts = x.toString().split(".");
  parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  return parts.join(".");
}

function agregarError(etiqueta, error){
    $("#"+etiqueta).parent().addClass("has-error");
    $("#"+etiqueta).attr("title", error);
    $("#"+etiqueta).tooltip();
}

function removerError(etiqueta){
    $("#"+etiqueta).parent().removeClass("has-error");
    $("#"+etiqueta).attr("title", "");
    $("#"+etiqueta).tooltip("destroy");
}

/* Configuración CSRF Token AJAX */
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
      }
    }
  }
  return cookieValue;
}
function csrfSafeMethod(method) {
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function ajax() {
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      }
    }
  });
}

/* JS Util */
function convertir_decimal_a_moneda(str) {
  if (!isNaN(str)) {
    if (str === parseInt(str) || str === parseFloat(str)) {
      str = str.toString();
    }
    str = str.replace(" ","").replace(",","").replace("$","");
    if (str.indexOf(".") == -1) {
      str += ".00";
    } else {
      if (str.indexOf(".") == str.length - 1) {
        str += "00";
      } else if (str.indexOf(".") == str.length - 2) {
        str += "0";
      }
    }
  } else {
    str = "0.00";
  }
  return "$ "+str;
}

function convertir_moneda_a_decimal(str) {
  str = str.replace(" ","").replace(",","").replace("$","");
  if (str.indexOf(".") != -1) {
    if (str.indexOf(".") == str.length - 1) {
      return str.replace(".", "");
    } else if (str.indexOf(".") == str.length - 2) {
      return str.replace(".0", "");
    } else {
      return str.replace(".00", "");
    }
  }
  return str;
}

function intcomma(str) {
  if(str) {
    if (str === parseInt(str) || str === parseFloat(str)) {
      str = str.toString();
    }
    var partes = str.trim().replace("$","").split(".");
    str = partes[0].replace(/,/g,"");
    partes[0] = parseFloat(str).toLocaleString("en-EU");
    if (partes.length == 2) {
      if (partes[1].length == 1) {
        partes[1] += "0";
      }
    }else {
      return partes[0] + ".00";
    } 
    return partes.join(".");
  } else {
    return "0.00";
  }
}


function getCaretPosition (oField) {
  var iCaretPos = 0;
  if (document.selection) {
    var oSel = document.selection.createRange ();
    oSel.moveStart ('character', -oField.value.length);
    iCaretPos = oSel.text.length;
  } else if (oField.selectionStart || oField.selectionStart == '0') {
    iCaretPos = oField.selectionStart;
  }
  return iCaretPos;
}

function setSelectionRange(input, selectionStart, selectionEnd) {
  if (input.setSelectionRange) {
    input.setSelectionRange(selectionStart, selectionEnd);
  }
  else if (input.createTextRange) {
    var range = input.createTextRange();
    range.collapse(true);
    range.moveEnd('character', selectionEnd);
    range.moveStart('character', selectionStart);
    range.select();
  }
}

function setCaretToPosition(input, pos) {
  setSelectionRange(input, pos, pos);
}