function showTab(n) {
  // This function will display the specified tab of the form...
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "block";
  //... and fix the Previous/Next buttons:
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == (x.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "Section suivante";
  } else {
    document.getElementById("nextBtn").innerHTML = "Suivant";
  }
  //... and run a function that will display the correct step indicator:
  fixStepIndicator(n)
}

function nextPrev(n) {
  // This function will figure out which tab to display
  var x = document.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && !validateForm()) return false;
  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form...
  if (currentTab >= x.length) {
    // ... the form gets submitted:
    document.getElementById("regForm").submit();
    return false;
  }
  // Otherwise, display the correct tab:
  showTab(currentTab);
}

function validateForm() {
  // This function deals with validation of the form fields
  var x, y, z, radio, i, valid = true;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");
  z = x[currentTab].getElementsByTagName("select");
  // A loop that checks every input field in the current tab:
  radio = x[currentTab].querySelectorAll('input[type="radio"]');
  for (i = 0; i < y.length; i++) {
    // If a field is empty...
    if (y[i].value == ""){
        if (y[i].className == "cond") {
          valid = true;
        }else{
          // add an "invalid" class to the field:
          y[i].className += " invalid";
          // and set the current valid status to false
          valid = false;
        }
    }
    }

  for (i = 0; i < z.length; i++) {
    // If a field is empty...
    if (z[i].value == ""){
        if (z[i].className == "cond") {
          valid = true;
        }else{
          // add an "invalid" class to the field:
          z[i].className += " invalid";
          // and set the current valid status to false
          valid = false;
        }
    }
  }  // If the valid status is true, mark the step as finished and valid:
  if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
  }else{
    alert("Vous n'avez pas répondu à toutes les questions. Vérifiez les boutons et cases a cocher");
  }
  return valid; // return the valid status
}

function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var i, x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  //... and adds the "active" class on the current step:
  x[n].className += " active";
}

$(function() {
	$("input[id^=row-]").blur(function(){
		var reg = new RegExp("X", "");
		res = this.id.split(reg);
		var valeurcible=res[2];
		var relation=res[1];
		var enfant=res[0];
		var valeurcible2;
		if(valeurcible == "vide"){
			valeurcible2="";
		}else{
			valeurcible2=valeurcible;
			}
		if (relation == 'eq'){
			if($(this).val() == valeurcible2) {
				$('.child-'+enfant+relation+valeurcible).show();
			}else{
				$('.child-'+enfant+relation+valeurcible).hide();
			}
		}else{
			if($(this).val() != valeurcible2){
				$('.child-'+enfant+relation+valeurcible).show();
			}else{
				$('.child-'+enfant+relation+valeurcible).hide();
			}
		}
	});
});

$(function() {
	$("input[id^=row-]").click(function(){
		var reg = new RegExp("X", "");
		res = this.id.split(reg);
		var valeurcible=res[2];
		var relation=res[1];
		var enfant=res[0];
		var valeurcible2;
		var courant=$(this).val();
		if(valeurcible=="vide"){
			valeurcible2="";
		}else{
			valeurcible2= valeurcible;
			valeurcible=parseInt(valeurcible, 10);
			courant=parseInt(courant, 10);
			valeurcible2=parseInt(valeurcible2, 10);
			}
		if (relation=='eq'){
			if(courant == valeurcible2) {
					$('.child-'+enfant+relation+valeurcible).show();
			}else{
					$('.child-'+enfant+relation+valeurcible).hide();
			}
		}else if(relation=='inf'){
			if(courant < valeurcible2) {
					$('.child-'+enfant+relation+valeurcible).show();
			}else{
					$('.child-'+enfant+relation+valeurcible).hide();
			}
		}else if(relation=='sup'){
			if(courant > valeurcible2) {
					$('.child-'+enfant+relation+valeurcible).show();
			}else{
					$('.child-'+enfant+relation+valeurcible).hide();
			}
		}else if(relation == 'diff'){
			if(courant != valeurcible2) {
					$('.child-'+enfant+relation+valeurcible).show();
			}else{
					 $('.child-'+enfant+relation+valeurcible).hide();
			}
		}
	});
});

$(function() {
$("select[id^=row-]").click(function(){
	var reg = new RegExp("X", "");
	res = this.id.split(reg);
	var valeurcible=res[2];
	var relation=res[1];
	var enfant=res[0];
	var courant=$(this).val();
	if(valeurcible=="vide"){
			valeurcibl2="";
	}
    valeurcible=parseInt(valeurcible, 10);
    courant=parseInt(courant, 10);
	if (relation=='eq'){
		if(courant == valeurcible) {
			$('.child-'+enfant+relation+valeurcible).show();
		}else{
			$('.child-'+enfant+relation+valeurcible).hide();
		}
		}else if(relation =='inf'){
			if(courant < valeurcible) {
					$('.child-'+enfant+relation+valeurcible).show();
			}else{
					$('.child-'+enfant+relation+valeurcible).hide();
			}
		}else if(relation == 'sup'){
			if(courant > valeurcible) {
					$('.child-'+enfant+relation+valeurcible).show();
			}else{
					$('.child-'+enfant+relation+valeurcible).hide();
			}
		}else{
			if(courant != valeurcible){
				$('.child-'+enfant+relation+valeurcible).show();
			}else{
				$('.child-'+enfant+relation+valeurcible).hide();
			}
		}
	});
});
