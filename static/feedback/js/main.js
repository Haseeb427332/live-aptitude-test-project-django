function Login(){
    var u = document.getElementById('username').value
    var p = document.getElementById('password').value
    if (u.length == 0)
    {
        alert('username should not be empty')
        return false
    }
    else{
        if (p.length == 0)
    {
        alert ('password should not be empty')
        return false
    }
    }
  }

function passwordverify(){
  var password= document.querySelector('#password1')
  var conpassword = document.querySelector('#password2')
  if (password.value !== conpassword.value)
  {
    alert('Password did not match ');
    password.focus = true
    console.log("1");
    return false;
  }
  console.log("2");
  return true;
}

function head(){
  document.getElementById("head").style.visibility="true"
}

function save_alert(){
  alert('Please make sure to save if any test question entered before moving to the another page')
}

function ans_save(){
  alert('Your answer has been saved')
  document.getElementById("test").disabled = true;
}

function opt_value(){
  var ch1 = document.getElementById("opt1").value
  document.getElementById("opt1_val").innerHTML = ch1
  document.getElementById("opt1_val").value = ch1

  var ch2 = document.getElementById("opt2").value
  document.getElementById("opt2_val").innerHTML = ch2
  document.getElementById("opt2_val").value = ch2

  var ch3 = document.getElementById("opt3").value
  console.log(ch3)
  if(ch3.length == 0){
    document.getElementById("opt3_val").style.display="none"
  }
  else{
      document.getElementById("opt3_val").innerHTML = ch3;
      document.getElementById("opt3_val").value = ch3;
      document.getElementById("opt3_val").style.display="block"
  }
  var ch4 = document.getElementById("opt4").value
  if (ch4.length == 0){
    document.getElementById("opt4_val").style.display="none"
  }
  else{
    document.getElementById("opt4_val").innerHTML = ch4;
    document.getElementById("opt4_val").value = ch4;
    document.getElementById("opt4_val").style.display="block"
  }

  if (ch2){
    var hidden = document.getElementById("hidden")
  hidden.style.visibility = "visible";
  }
}

function ans_Delete(){
  alert('Test Questions has been Deleted')
}

function Search() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[3];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }       
  }
}

function add(){
  var ch3  = document.getElementById("opt3")
  var ch4 = document.getElementById("opt4")
  ch3.style.visibility = "visible"
  ch3.required = true;
  ch4.style.visibility = "visible"
  ch4.required = true;
  document.getElementById("add").style.display = "none"
}

function refresh(){
  location.reload()
}

function updateinfo(){
document.getElementById("firstname").disabled = false
document.getElementById("lastname").disabled = false
document.getElementById("email").disabled = false
document.getElementById("username").disabled = false
document.getElementById("department").disabled = false
document.getElementById("semster").disabled = false
document.getElementById("semster").disabled = false
document.getElementById("password1").disabled = false
document.getElementById("password2").disabled = false
document.getElementById("show").style.visibility = "visible"
document.getElementById("save").style.visibility = "visible"
document.getElementById("reset").style.visibility = "visible"
}

function show_txt(){
  document.getElementById("pass").style.visibility = "visible"
  document.getElementById("show").style.visibility = "hidden"
}

function timer(){
  var countdown = 10 * 60 * 1000;
  var timerId = setInterval(function(){
    countdown -= 1000;
    var min = Math.floor(countdown / (60 * 1000));
    var sec = Math.floor((countdown - (min * 60 * 1000)) / 1000);

    if (countdown <= 0) {
       alert("Time is UP!!!!!");
       document.forms["testform"].submit()
       clearInterval(timerId);
    } else {
       $("#timer").html(min + " : " + sec);
    }
  }, 1000);
}

$(document).ready(function(){
  $("#myModal").modal('show');
});

function openFullscreen() {
  var elem = document.documentElement;
  if (elem.requestFullscreen) {
    elem.requestFullscreen();
  } else if (elem.webkitRequestFullscreen) { /* Safari */
    elem.webkitRequestFullscreen();
  } else if (elem.msRequestFullscreen) { /* IE11 */
    elem.msRequestFullscreen();
  } ;
  $("#myModal").modal('hide');
}

function forget(){
  document.getElementById("forgot").style.visibility="visible"
  console.log('sfgr')
}

function saved(){
  alert('Password has been Successfully Updated')
}

