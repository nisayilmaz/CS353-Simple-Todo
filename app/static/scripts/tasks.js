async function getUnfinished() {
    var tabcontent = document.getElementsByClassName("tab-content");
    for(let i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";

    }
    
    var tablinks = document.getElementsByClassName("tab-link");
    for(let i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    document.getElementById("unfinished").style.display = "block";
    document.getElementById("unfinished-btn").className += " active";

    let response = await fetch('/unfinished_tasks');
    let data = await response.text();
    let addhtml = '';
    data = JSON.parse(data);
    data.forEach(element => {
        addhtml += `<tr>
                        <td>${element["title"]}</td>
                        <td>${element["description"]}</td>
                        <td>${element["status"]}</td>
                        <td>${element["deadline"]}</td>
                        <td>${element["creation_time"]}</td>
                        <td>${element["task_type"]}</td>
                    </tr>`
      
    });
    document.getElementById("unfinished-table").innerHTML = addhtml;

 
}

async function getFinished() {
    var tabcontent = document.getElementsByClassName("tab-content");
    for(let i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    
    var tablinks = document.getElementsByClassName("tab-link");
    for(let i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    document.getElementById("finished").style.display = "block";
    document.getElementById("finished-btn").className += " active";

    let addhtml = '';
    let response = await fetch('/finished_tasks');
    let data = await response.text();
    data = JSON.parse(data);
    data.forEach(element => {

        addhtml += `<tr>
            <td>${element["title"]}</td>
            <td>${element["description"]}</td>
            <td>${element["status"]}</td>
            <td>${element["deadline"]}</td>
            <td>${element["creation_time"]}</td>
            <td>${element["done_time"]}</td>
            <td>${element["task_type"]}</td>
         </tr>`
    
    });

    document.getElementById("finished-table").innerHTML = addhtml;


}

async function getAdd() {
    var tabcontent = document.getElementsByClassName("tab-content");
    for(let i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    
    var tablinks = document.getElementsByClassName("tab-link");
    for(let i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    document.getElementById("add").style.display = "block";
    document.getElementById("add-btn").className += " active";



}