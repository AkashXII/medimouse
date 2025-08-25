let currentUser = ""; 
let editMedId = null;

function hideAllPages() {
  document.getElementById("landing").style.display = "none";
  document.getElementById("signIn").style.display = "none";
  document.getElementById("signUp").style.display = "none";
  document.getElementById("dashboard").style.display = "none";
}

function landing() { hideAllPages(); document.getElementById("landing").style.display = "block"; }
function signin() { hideAllPages(); document.getElementById("signIn").style.display = "block"; }
function signup() { hideAllPages(); document.getElementById("signUp").style.display = "block"; }
function dashboard() { hideAllPages(); document.getElementById("dashboard").style.display = "block"; }

async function register() {
  const name = document.getElementById("signupName").value;
  const username = document.getElementById("signupUsername").value;
  const password = document.getElementById("signupPassword").value;
  const age = parseInt(document.getElementById("signupAge").value);
  const weight = parseFloat(document.getElementById("signupWeight").value);
  const height = parseFloat(document.getElementById("signupHeight").value);

  const res = await fetch("http://127.0.0.1:8000/users", {
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body: JSON.stringify({name, username, password, age, weight, height})
  });
  if(res.status===200 || res.status===201){ alert("Registered!"); signin(); }
  else { const err=await res.json(); alert("Error: "+err.detail); }
}

async function login() {
  const username = document.getElementById("loginUsername").value;
  const password = document.getElementById("loginPassword").value;

  const res = await fetch("http://127.0.0.1:8000/login", {
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body: JSON.stringify({username,password})
  });
  if(res.status===200){ 
    currentUser = username;
    document.getElementById("userWelcome").innerText = username;
    dashboard(); 
    loadMedicines();
    loadBMI();
  } else { const err=await res.json(); alert("Error: "+err.detail); }
}

function logout() { currentUser=""; editMedId=null; landing(); }

async function loadMedicines() {
  const res = await fetch(`http://127.0.0.1:8000/medicines/${currentUser}`);
  const data = await res.json();
  const list = document.getElementById("medList");
  list.innerHTML = "";
  data.forEach(med=>{
    const li = document.createElement("li");
    li.innerHTML = `${med.name} (${med.dosage}) at ${med.time} 
      <button onclick="editMedicine(${med.id},'${med.name}','${med.dosage}','${med.time}')">Edit</button>
      <button onclick="deleteMedicine(${med.id})">Delete</button>`;
    list.appendChild(li);
  });
}

async function saveMedicine() {
  const name = document.getElementById("medName").value;
  const dosage = document.getElementById("medDosage").value;
  const time = document.getElementById("medTime").value;

  if(editMedId){
    await fetch(`http://127.0.0.1:8000/medicines/${editMedId}`, {
      method:"PUT",
      headers:{"Content-Type":"application/json"},
      body: JSON.stringify({name,dosage,time})
    });
    editMedId = null;
  } else {
    await fetch(`http://127.0.0.1:8000/medicines?username=${currentUser}`, {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body: JSON.stringify({name,dosage,time})
    });
  }
  document.getElementById("medName").value="";
  document.getElementById("medDosage").value="";
  document.getElementById("medTime").value="";
  loadMedicines();
}

function editMedicine(id,name,dosage,time){
  editMedId=id;
  document.getElementById("medName").value=name;
  document.getElementById("medDosage").value=dosage;
  document.getElementById("medTime").value=time;
}

async function deleteMedicine(id){
  await fetch(`http://127.0.0.1:8000/medicines/${id}`,{method:"DELETE"});
  loadMedicines();
}

async function loadBMI(){
  const res = await fetch(`http://127.0.0.1:8000/users/${currentUser}/bmi`);
  const data = await res.json();
  document.getElementById("userBMI").innerText = data.bmi ? `${data.bmi} (${data.category})` : "-";
}
