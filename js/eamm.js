
function validateForm() {

	// get the invitees area.
	var inviteesArea=document.forms["addMeeting"]["invitees"].value;

	// create an array of each line, split by <br> tag.
	var inviteesArray = inviteesArea.split("<br>");

	var inviteesTmp = new Array();

	// iterate the list, discard HTML tags.
	for (var i = 0; i < inviteesArray.length; i++) {
	    var tmp = inviteesArray[i].replace(/<.*>/g,"");
	    console.log(inviteesArray[i]);
	    console.log(tmp);
    	inviteesTmp.push(inviteesArray[i].replace(/<.*>/g,""));
    	console.log(inviteesTmp[i]);
	}

  	return false;
 }
