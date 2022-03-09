document.addEventListener('DOMContentLoaded', function () {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));

  document.querySelector('#compose').addEventListener('click', new_email);
  document.querySelector('#compose-form').addEventListener('submit', event => {
    event.preventDefault();
    send_email();
  });
  load_mailbox('inbox');
});


//Loads mailboxes
function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#content_body').style.display = 'none';
  document.querySelector('#archive_email').style.display = 'block';
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      emails_view = document.querySelector('#emails-view');
      var maillist = document.createElement("div");
      maillist.className = "container";
      emails_view.appendChild(maillist);

      let row = document.createElement("div");
      row.className = "row";
      row.id = "MailHeader"

      if (emails.length === 0) {

        let warning = document.createElement("div");
        var text = document.createTextNode("You have no mail in the box!");
        warning.appendChild(text);
        row.appendChild(warning)
        maillist.appendChild(row)
      }
      else {
        //Loops a mail,first is prefered, to get needed headings
        for (let key of Object.keys(emails[0])) {
          //This function creates headers for mailbox
          if (key === "sender" || key === "subject" || key === "timestamp") {

            let header = document.createElement("div");

            if (key === "sender") {
              header.className = "col-3";
              var text = document.createTextNode("From");
            }
            else if (key === "subject") {
              header.className = "col-6";
              var text = document.createTextNode("Subject");
            }
            else if (key === "timestamp") {
              header.className = "col-3";
              var text = document.createTextNode("Date");
            }

            header.appendChild(text);
            row.appendChild(header)
          }

        }
        maillist.appendChild(row)

        //creates row for each mail.then adds values for related mail.From, Subject, timestamp
        for (let step = 0; step < emails.length; step++) {
          let row = document.createElement("div");
          row.className = "row border mailRow";
          row.id = emails[step].id
          row.style.cursor = "pointer"

          //Checks whether a mail is read before or not.
          if (emails[step].read == true) {
            row.style.backgroundColor = "#eeeeee"
          }

          //for a single row
          for (var [index, [key, value]] of Object.entries(Object.entries(emails[step]))) {

            if (key === "sender" || key === "subject" || key === "timestamp") {
              var col = document.createElement("div");
              var text = document.createTextNode(`${value}`);
              if (key === "sender") {
                col.className = "col-3";
              }
              else if (key === "subject") {
                col.className = "col-6";
              }
              else if (key === "timestamp") {
                col.className = "col-3";
              }


              col.appendChild(text);
              row.appendChild(col);
              maillist.appendChild(row);
            }
          }

        }

        //Adds eventlisteners for each row in maillist.
        var x = document.getElementsByClassName('mailRow');
        for (var i = 0; i < x.length; i++) {
          x[i].addEventListener('click', check);
        }
      }

    }
    )

    if(mailbox==="sent"){
      document.querySelector('#archive_email').style.display = 'none';
    }
}
//Loads first message page
function new_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#content_body').style.display = 'none';
  document.getElementById("compose_header").innerHTML = "New Email";
  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

//Checks if clicked area is a mail row.
function check(event) {
  const element = event.target;
  var closest = element.closest(".mailRow");
  if (closest) {
    var mail_id = parseInt(closest.id)
    content(mail_id)
  }
}
//load mail content when clicked on a mailrow
function content(mail_id) {
  fetch(`/emails/${mail_id}`)
    .then(response => response.json())
    .then(email => {
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('#content_body').style.display = 'block';

      document.getElementById("mailFrom").innerHTML = email.sender;
      document.getElementById("mailRecipients").innerHTML = email.recipients;
      document.getElementById("mailSubject").innerHTML = email.subject;
      document.getElementById("mailTimestamp").innerHTML = email.timestamp;
      // document.getElementById("mailBody").innerHTML = email.body;
      document.getElementById("mailBody").innerText = email.body
      document.getElementById('reply_email').addEventListener('click', () => reply_email(email))
      document.getElementById('archive_email').addEventListener('click', () => {
        archive_email(email)
      }, { once: true })
      //Shows archieving button in accordance with archieved status of the mail.
      if (email.archived == false) {
        document.getElementById("archive_email").innerText = "Archieve"
      }
      else {
        document.getElementById("archive_email").innerText = "Unarchieve"
      }

      //if mail is not read, then sends a put request to make it read true in the model database.
      if (email.read == false) {
        fetch(`/emails/${mail_id}`, {
          method: 'PUT',
          body: JSON.stringify({
            read: true
          })
        })
      }
    });
}

function archive_email(email) {
  if (email.archived == false) {
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: true
      })
    })
  }
  else {
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: false
      })
    })

  }
  setTimeout(function () { load_mailbox('inbox'); }, 100)
}
//loads reply page for a clicked mail.
function reply_email(email) {

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#content_body').style.display = 'none';
  document.getElementById("compose_header").innerHTML = "Reply Email";

  var to = email.sender;
  var about = email.subject;
  var message = email.body
  var timestamp = email.timestamp;
  if (about.indexOf("Re:") === 0) {
    document.querySelector('#compose-subject').value = about;
  }
  else {
    document.querySelector('#compose-subject').value = "Re: " + about;

  }

  document.querySelector('#compose-recipients').value = to;

  document.querySelector('#compose-body').value = "\n\n\n\n" + "On " + timestamp + ", " + to + " wrote: " + "\n" + message;
}

//sends mail from compose view.
function send_email() {
  var to = document.querySelector("#compose-recipients").value;
  var about = document.querySelector("#compose-subject").value;
  var message = document.querySelector("#compose-body").value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: to,
      subject: about,
      body: message
    })
  })

    .then(response => response.json())
    .then(result => {
      // Print result
      console.log(result);
    });
  setTimeout(function () { load_mailbox('sent'); }, 100)
}




