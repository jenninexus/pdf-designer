'use strict';
window.fixtureEvents = {input:0,change:0,submits:0,files:0};
document.addEventListener('input',()=>window.fixtureEvents.input++);
document.addEventListener('change',e=>{window.fixtureEvents.change++; if(e.target.type==='file') window.fixtureEvents.files++;});
document.addEventListener('submit',e=>{e.preventDefault();window.fixtureEvents.submits++;});
