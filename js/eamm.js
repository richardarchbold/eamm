
// The step3 form has:
//  * start date
//  * start time
//  * duration
//  * repeats
//  * end date
//  * venue
//  * requester
//  * invitees
function validateStep3Form() {

	tinyMCE.triggerSave();

    if (validateInvitees()) {
        return true;
    } else {
        return false;
    }

}

// validating invitees:
// - split the context of the textarea, by using the <br> tag.
// - put the output of the split into an array.
// - strip out all the other html.
// - regex whatever is left and match against an email addr.
function validateInvitees() {

    // get the invitees area.
    var inviteesArea=document.forms["add_meeting_invite"]["invitees"].value;

    // create an array of each line, unfortunately, it seems that sometimes a
    // newline is represented by a <br> and sometimes by a '\n'.
    var tmpArray = new Array();
    tmpArray = inviteesArea.split(/<br.*?>|\n/);

    // iterate the list
    for (var i = 0; i < tmpArray.length; i++) {
        // discard remaining HTML tags.
        tmpArray[i] = tmpArray[i].replace(/<.*?>/g,"");

        // save the nice non-HTML tagged text to show as as error if this line proves to not be a
        // well formed email address.
        var tmpForError = tmpArray[i]

        // strip whitespace.
        // &nbsp;
        tmpArray[i] = tmpArray[i].replace(/&nbsp;/g,"");
        tmpArray[i] = tmpArray[i].replace(/&nbsp/g,"");
        tmpArray[i] = tmpArray[i].replace(/^\W*?/g,"");
        tmpArray[i] = tmpArray[i].replace(/\W*?$/g,"");


        // check to see if whatever remains looks like an email address
        // alert to the user and return false if not.
        var email_regex = /^[\w\-\.]+@[\w\.\-]+\.\w+$/;
        if (! email_regex.test(tmpArray[i])) {
            alert("Line: \"" + tmpForError + "\" in the invitees list does not seem like an email address :-(");
            return false;
        }
    }

    return true;
}
