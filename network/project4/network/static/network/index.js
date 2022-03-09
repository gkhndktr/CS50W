document.addEventListener('DOMContentLoaded', function () {
    var textarea = document.getElementById("postText")
    textarea.value=""
    document.getElementsByName("like").forEach(function (currentValue, event) {
        currentValue.addEventListener("click", (event) => {

            PostId= event.target.closest("[name~=post]").id
            like();
        })
    });
    document.getElementsByName("edit").forEach(function (currentValue, event) {
        currentValue.addEventListener("click", (event) => {
            PostId= event.target.closest("[name~=post]").id
            edit(event);
        })
    });
    document.getElementById("submit_edit").addEventListener("click", event => {
        event.preventDefault();
        editSubmit();
    });

    textarea.addEventListener("input", event => {
        const target = event.currentTarget;
        const maxLength = target.getAttribute("maxlength");
        const currentLength = target.value.length;
    
        if (currentLength >= maxLength) {
            document.getElementById("postText").style.color="red";
            alert("You can only have 140 characters.")
            document.getElementById("postText").style.color="";
            return console.log("You have reached the maximum number of characters.");
        }
        else{
            document.getElementById("postText").style.color=""
        }
        
        console.log(`${maxLength - currentLength} chars left`);
    });
});
var PostId=""
var empty = "m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"
var fill = "M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"

async function like() {

    if (document.getElementById("h" + PostId).getAttribute("d") == empty) {
        let promise = fetch(`/like/${PostId
            }`, { method: "PUT" })
            let result = await promise;
        console.log(result)
        let count = parseInt(document.getElementById("l" + PostId).innerText)
        document.getElementById("l" + PostId).innerText = count + 1
        document.getElementById("h" + PostId).setAttribute("d", fill)
    }
    else {
        let promise = fetch(`/unlike/${PostId
            }`, { method: "PUT" })
            let result = await promise;
        console.log(result)
        let count = parseInt(document.getElementById("l" + PostId).innerText)
        document.getElementById("l" + PostId).innerText = count - 1
        document.getElementById("h" + PostId).setAttribute("d", empty)
    }
};

function edit(event){
    var id = event.target.id.slice(1)
    var post=document.getElementById("p"+id).innerText
    var submit=document.getElementById(event.target.id)
    document.getElementById("message-text").value=post
    console.log(post)
}


async function editSubmit() {
    var text = document.getElementById("message-text").value;
    var myfetch = fetch(`../edit/${PostId}`, {
        method: 'PUT',
        body: JSON.stringify(
            { post: text }
        )
    });

    var response = await myfetch;
    console.log(response)
    document.getElementById("p"+PostId).value=text;
    document.getElementById("message-text").value="";
    document.getElementById("p"+PostId).innerHTML=text
}