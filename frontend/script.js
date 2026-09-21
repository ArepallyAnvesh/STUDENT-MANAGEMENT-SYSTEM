const API="http://127.0.0.1:5000";

function loadDashboard(){
fetch(API+"/dashboard")
.then(response=>{
if(!response.ok){
throw new Error("Server error");
}
return response.json();
})
.then(data=>{
document.getElementById("totalStudents").innerText=data.total_students;
document.getElementById("qualifiedStudents").innerText=data.qualified_students;
document.getElementById("failedStudents").innerText=data.failed_students;
document.getElementById("topper").innerText=data.topper;
})
.catch(error=>{
console.log(error);
});
}

function loadStudents(){
fetch(API+"/students")
.then(response=>response.json())
.then(data=>{
let table=document.getElementById("studentTable");

if(!table)return;

table.innerHTML="";

data.forEach(student=>{
table.innerHTML+= `
<tr>
<td>${student.student_id}</td>
<td>${student.student_name}</td>
<td>${student.maths}</td>
<td>${student.statistics}</td>
<td>${student.computer_science}</td>
<td>${student.english}</td>
<td>${student.hr_ethics}</td>
</tr> `;
});
})
.catch(error=>console.log(error));
}

document.getElementById("studentForm")?.addEventListener("submit",function(e){

e.preventDefault();

let data={
student_name:document.getElementById("name").value,
maths:document.getElementById("maths").value,
statistics:document.getElementById("statistics").value,
computer_science:document.getElementById("computer_science").value,
english:document.getElementById("english").value,
hr_ethics:document.getElementById("hr_ethics").value
};

fetch(API+"/students",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify(data)
})
.then(response=>response.json())
.then(result=>{
document.getElementById("message").innerText=result.message;
document.getElementById("studentForm").reset();
})
.catch(error=>{
document.getElementById("message").innerText="Error connecting to server";
console.log(error);
});

});

document.getElementById("searchForm")?.addEventListener("submit",function(e){

e.preventDefault();

let search=document.getElementById("search").value;

fetch(API+"/search/"+encodeURIComponent(search))
.then(response=>response.json())
.then(data=>{

let result=document.getElementById("searchResult");

if(data.length===0){
result.innerHTML="<p>Student not found</p>";
return;
}

result.innerHTML=`
<table>
<thead>
<tr>
<th>ID</th>
<th>Name</th>
<th>Maths</th>
<th>Statistics</th>
<th>Computer Science</th>
<th>English</th>
<th>HR & Ethics</th>
</tr>
</thead>
<tbody>
${data.map(student=>`
<tr>
<td>${student.student_id}</td>
<td>${student.student_name}</td>
<td>${student.maths}</td>
<td>${student.statistics}</td>
<td>${student.computer_science}</td>
<td>${student.english}</td>
<td>${student.hr_ethics}</td>
</tr>
`).join("")}
</tbody>
</table>
`;

})
.catch(error=>{
document.getElementById("searchResult").innerHTML="<p>Error connecting to server</p>";
console.log(error);
});

});

document.getElementById("updateForm")?.addEventListener("submit",function(e){

e.preventDefault();

let id=document.getElementById("student_id").value;

let data={
student_name:document.getElementById("student_name").value,
maths:document.getElementById("maths").value,
statistics:document.getElementById("statistics").value,
computer_science:document.getElementById("computer_science").value,
english:document.getElementById("english").value,
hr_ethics:document.getElementById("hr_ethics").value
};

fetch(API+"/students/"+id,{
method:"PUT",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify(data)
})
.then(response=>response.json())
.then(result=>{
document.getElementById("message").innerText=result.message;
})
.catch(error=>{
document.getElementById("message").innerText="Error connecting to server";
console.log(error);
});

});

document.getElementById("deleteForm")?.addEventListener("submit",function(e){

e.preventDefault();

let id=document.getElementById("student_id").value;

let confirmDelete=confirm("Do you want to delete this student?");

if(!confirmDelete){
return;
}

fetch(API+"/students/"+id,{
method:"DELETE"
})
.then(response=>response.json())
.then(result=>{
document.getElementById("message").innerText=result.message;
document.getElementById("deleteForm").reset();
})
.catch(error=>{
document.getElementById("message").innerText="Error connecting to server";
console.log(error);
});

});

function loadResults(){

fetch(API+"/results")
.then(response=>response.json())
.then(data=>{

let table=document.getElementById("resultsTable");

if(!table)return;

table.innerHTML="";

data.forEach(student=>{

table.innerHTML+=`
<tr>
<td>${student.student_id}</td>
<td>${student.student_name}</td>
<td>${student.total}</td>
<td>${student.percentage}%</td>
<td>${student.grade}</td>
<td>${student.status}</td>
</tr>
`;

});

})
.catch(error=>console.log(error));

}

function loadTopper(){

fetch(API+"/topper")
.then(response=>response.json())
.then(student=>{

let result=document.getElementById("topperResult");

if(!result)return;

result.innerHTML=`
<div class="result-box">
<div class="result">
<h2>${student.student_name}</h2>
<p>Student ID: ${student.student_id}</p>
<p>Total Marks: ${student.total} / 500</p>
<p>Percentage: ${student.percentage}%</p>
<p>Grade: ${student.grade}</p>
</div>
</div>
`;

})
.catch(error=>console.log(error));

}

function loadQualified(){

fetch(API+"/qualified")
.then(response=>response.json())
.then(data=>{

let table=document.getElementById("qualifiedTable");

if(!table)return;

table.innerHTML="";

data.forEach(student=>{

table.innerHTML+=`
<tr>
<td>${student.student_id}</td>
<td>${student.student_name}</td>
<td>${student.maths}</td>
<td>${student.statistics}</td>
<td>${student.computer_science}</td>
<td>${student.english}</td>
<td>${student.hr_ethics}</td>
<td>${student.total}</td>
<td>${student.percentage}%</td>
</tr>
`;

});

})
.catch(error=>console.log(error));

}

function loadFailed(){

fetch(API+"/failed")
.then(response=>response.json())
.then(data=>{

let table=document.getElementById("failedTable");

if(!table)return;

table.innerHTML="";

data.forEach(student=>{

table.innerHTML+=`
<tr>
<td>${student.student_id}</td>
<td>${student.student_name}</td>
<td>${student.maths}</td>
<td>${student.statistics}</td>
<td>${student.computer_science}</td>
<td>${student.english}</td>
<td>${student.hr_ethics}</td>
<td>${student.total}</td>
<td>${student.percentage}%</td>
</tr>
`;

});

})
.catch(error=>console.log(error));

}

if(document.getElementById("totalStudents")){
loadDashboard();
}

if(document.getElementById("studentTable")){
loadStudents();
}

if(document.getElementById("resultsTable")){
loadResults();
}

if(document.getElementById("topperResult")){
loadTopper();
}

if(document.getElementById("qualifiedTable")){
loadQualified();
}

if(document.getElementById("failedTable")){
loadFailed();
}