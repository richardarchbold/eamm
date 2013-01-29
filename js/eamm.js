
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

window.onload = function() {
    // set onfocus and onblur events for anything that we care about.

    //purpose textarea
    if (document.getElementById("purpose")) {
        var purposeField = document.getElementById("purpose");

        purposeField.onfocus = function() {
            if (purposeField.value == "The purpose of this meeting is to XXX such that YYY can be achieved.") {
                purposeField.value = "";
            }
        };

        purposeField.onblur = function() {
            if ( purposeField.value == "") {
                purposeField.value = "The purpose of this meeting is to XXX such that YYY can be achieved.";
            }
        };
    }


    //justification textarea
    if (document.getElementById("justification")) {
        var justificationField = document.getElementById("justification");

        justificationField.onfocus = function() {
            if (justificationField.value == "A meeting is the best way to achieve my purpose because ...") {
                justificationField.value = "";
            }
        };

        justificationField.onblur = function() {
            if ( justificationField.value == "") {
                justificationField.value = "A meeting is the best way to achieve my purpose because ...";
            }
        };
    }

    //start_date text
    if (document.getElementById("start_date")) {
        var start_dateField = document.getElementById("start_date");

        start_dateField.onfocus = function() {
            if (start_dateField.value == "yyyy-mm-dd") {
                start_dateField.value = "";
            }
        };

        start_dateField.onblur = function() {
            if ( start_dateField.value == "") {
                start_dateField.value = "yyyy-mm-dd";
            }
        };
    }

    //start_time text
    if (document.getElementById("start_time")) {
        var start_timeField = document.getElementById("start_time");

        start_timeField.onfocus = function() {
            if (start_timeField.value == "hh:mm") {
                start_timeField.value = "";
            }
        };

        start_timeField.onblur = function() {
            if ( start_timeField.value == "") {
                start_timeField.value = "hh:mm";
            }
        };
    }

    //duration text
    if (document.getElementById("duration")) {
        var durationField = document.getElementById("duration");

        durationField.onfocus = function() {
            if (durationField.value == "mm") {
                durationField.value = "";
            }
        };

        durationField.onblur = function() {
            if ( durationField.value == "") {
                durationField.value = "mm";
            }
        };
    }

    //end_date text
    if (document.getElementById("end_date")) {
        var end_dateField = document.getElementById("end_date");

        end_dateField.onfocus = function() {
            if (end_dateField.value == "yyyy-mm-dd") {
                end_dateField.value = "";
            }
        };

        end_dateField.onblur = function() {
            if ( end_dateField.value == "") {
                end_dateField.value = "yyyy-mm-dd";
            }
        };
    }

    //requester text
    if (document.getElementById("requester")) {
        var requesterField = document.getElementById("requester");

        requesterField.onfocus = function() {
            if (requesterField.value == "you@example.com") {
                requesterField.value = "";
            }
        };

        requesterField.onblur = function() {
            if ( requesterField.value == "") {
                requesterField.value = "you@example.com";
            }
        };
    }

};
