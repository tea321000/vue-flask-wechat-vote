/**
 * Created by jiachenpan on 16/11/18.
 */

export function isExternal(path) {
  return /^(https?:|mailto:|tel:)/.test(path)
}

export function validUsername(str) {
  // const valid_map = ['admin', 'editor']
  // return valid_map.indexOf(str.trim()) >= 0
  const reg = /^[0-9]{6,10}$/
  return reg.test(str)
}

export function validPassword(str) {

  const reg = /^[a-zA-Z0-9\~\!\@\#\$\%\^\&\*\_\+\{\}\:\"\|\<\>\?\-\=\;\'\\\,\.\/]{6,15}$/
  return reg.test(str)
}


export function validPhone(str) {
  const reg = /^(0\d{2,3}[-| ]?)?(\d{7,8})([-| ]?\d{3,5})?$/
  return reg.test(str)
}

export function validName(str) {
  const reg = /^([\u4e00-\u9fa5]{2,4})$/
  return reg.test(str)
}
export function validBirthday(str) {
  if (!str)
    return false;
  else
    return true;
}

export function validBlank(str) {
  if (!str)
    return false;
  else
    return true;
}

export function validDate(startDate1, startDate2, endDate1, endDate2) {
  if (!startDate1 || !startDate2 || !endDate1 || !endDate2) {
    // console.log(startDate1)
    // console.log(startDate2)
    // console.log(endDate1)
    // console.log(endDate2)

    return false;

  } else {
    var Date1 = new Date(startDate1);
    var Date2 = new Date(endDate1);
    if (Date1.getTime() < Date2.getTime())
      return true;
    else if (Date1.getTime() == Date2.getTime()) {
      var hour = startDate2.split(':')[0];
      var min = startDate2.split(':')[1];
      var sec = startDate2.split(':')[2];

      var Date3 = Number(hour * 3600) + Number(min * 60) + Number(sec);
      var hour = endDate2.split(':')[0];
      var min = endDate2.split(':')[1];
      var sec = endDate2.split(':')[2];

      var Date4 = Number(hour * 3600) + Number(min * 60) + Number(sec);
      if (Date4 > Date3)
        return true
      else
        return false

    } else
      return false;


  }

}
export function validSelected(length) {
  if (length < 1)
    return false
  else
    return true

}

export function validURL(url) {
  const reg = /^(https?|ftp):\/\/([a-zA-Z0-9.-]+(:[a-zA-Z0-9.&%$-]+)*@)*((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])){3}|([a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.(com|edu|gov|int|mil|net|org|biz|arpa|info|name|pro|aero|coop|museum|[a-zA-Z]{2}))(:[0-9]+)*(\/($|[a-zA-Z0-9.,?'\\+&%$#=~_-]+))*$/
  return reg.test(url)
}

export function validLowerCase(str) {
  const reg = /^[a-z]+$/
  return reg.test(str)
}

export function validUpperCase(str) {
  const reg = /^[A-Z]+$/
  return reg.test(str)
}

export function validAlphabets(str) {
  const reg = /^[A-Za-z]+$/
  return reg.test(str)
}

export function validEmail(email) {
  const reg = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  return reg.test(email)
}

export function isString(str) {
  if (typeof str === 'string' || str instanceof String) {
    return true
  }
  return false
}

export function isArray(arg) {
  if (typeof Array.isArray === 'undefined') {
    return Object.prototype.toString.call(arg) === '[object Array]'
  }
  return Array.isArray(arg)
}