//
// put everything inside this function, it's like main()
//
function prepareEventHandlers () {

	/*
	var myPurpose = document.getElementById("purpose");

	// onfocus, we zero it.
	myPurpose.onfocus = function() {
		if (myPurpose.value == "The purpose of this meeting is XXX such that YYY can be achieved.") {
			myPurpose.value = "";
		}
	}
	
	myPurpose.onblur = function() {
		if (myPurpose.value == "") {
			myPurpose.value = "The purpose of this meeting is XXX such that YYY can be achieved.";
		}
	}
	
	var myJustification = document.getElementById("justification");
	
	// onfocus, we zero it.
	myJustification.onfocus = function() {
		if (myJustification.value == "I have thought about it, and a meeting is the best option because ...") {
			myJustification.value = "";
		}
	}
	
	myJustification.onblur = function() {
		if (myJustification.value == "") {
			myJustification.value = "I have thought about it, and a meeting is the best option because ...";
		}
	}
	
	var myStartDate = document.getElementById("start_date");
	
	myStartDate.onfocus = function() {
		if (myStartDate.value == "yyyy-mm-dd") {
			myStartDate.value = "";
		}
	}
	
	myStartDate.onblur = function() {
		if (myStartDate.value == "") {
			myStartDate.value = "yyyy-mm-dd"
		} else {
			var dateRegex = /^\d\d\d\d-\d\d-\d\d$/
			
			if (! dateRegex.test(myStartDate.value)) {
				
				alert("Start Date must be in the format yyyy-mm-dd")
				myStartDate.value = "yyyy-mm-dd"
			}
		}

	}
	
	*/
	// var text = tinyMCE.get('myeditorid').getContent();
	//var myInvitees = document.getElementById("invitees");
	// Put each invitee email addr on a new line, eg<br>a@a.com<br>b@b.com
	
	var myInvitees = tinyMCE.get('invitees').getContent();
	
	// Sets the content of a specific editor (my_editor in this example)
	//tinyMCE.activeEditor.setContent("Blah, blah, blah");
		
	alert(myInvitees);
	
	
	/*
	myInvitees.onfocus = function() {
		if (myInvitees.value == "Put each invitee email addr on a new line, eg<br>a@a.com<br>b@b.com") {
			myInvitees.value = "";
		}
	}
	
	myInvitees.onblur = function() {
		if (myInvitees.value == "") {
			myInvitees.value = "Put each invitee email addr on a new line, eg<br>a@a.com<br>b@b.com";
		}
	}
	*/
}

window.onload = function() {
	prepareEventHandlers();
}
