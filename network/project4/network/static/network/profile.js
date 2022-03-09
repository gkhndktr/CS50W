document.addEventListener('DOMContentLoaded', function () {

    if (document.getElementsByName("follow")[0]){
        document.getElementsByName("follow")[0].addEventListener("click", (event) => {
            follow(event);
        });
    };
    document.getElementsByName("like").forEach(function (currentValue, event) {
        currentValue.addEventListener("click", (event) => {

            PostId= event.target.closest("[name~=post]").id
            like(PostId);
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
});
var PostId=""
var empty = "m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"
var fill = "M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"

function follow(event) {
    var element= event.target
    if(element.innerHTML=="Follow"){
    fetch(`../follow/${element.id}`, {
        method: 'GET'})  
    element.innerHTML="Unfollow";
    var follower= parseInt(document.getElementsByName("follower")[0].innerHTML)
    document.getElementsByName("follower")[0].innerHTML=follower+1
    }
    else{
    fetch(`../unfollow/${element.id}`, {
        method: 'GET'})  
    element.innerHTML="Follow";
    var follower= parseInt(document.getElementsByName("follower")[0].innerHTML)
    document.getElementsByName("follower")[0].innerHTML=follower-1
    };
    
    };
async function like(PostId) {
    console.log(PostId)
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
    var post=document.getElementById("p"+PostId).innerText
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