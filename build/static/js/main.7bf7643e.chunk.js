(this.webpackJsonpvaxthuset_frontend=this.webpackJsonpvaxthuset_frontend||[]).push([[0],{18:function(e,t,a){e.exports=a(53)},30:function(e,t,a){e.exports=a.p+"static/media/GloriaHallelujah-Regular.779caa76.ttf"},31:function(e,t,a){},32:function(e,t,a){},33:function(e,t,a){},34:function(e,t,a){},35:function(e,t,a){},53:function(e,t,a){"use strict";a.r(t);var n=a(0),r=a.n(n),l=a(16),c=a.n(l),o=a(6),u=function(){return r.a.createElement("div",{className:"header"})},i=function(){return r.a.createElement("div",{className:"footer"},r.a.createElement("ul",null,r.a.createElement("li",null,"App made by: Erik Liljeroth"),r.a.createElement("li",null," LinkedIn: ",r.a.createElement("a",{href:"https://www.linkedin.com/in/erikliljeroth/"},"Erik Liljeroth"))))},m=a(2),d=a(5),h=a.n(d),p=function(e){var t=e.data,a=e.className,n=t.map((function(e){return e.dtg})),l=t.map((function(e){return Number(e.temperature)})),c=t.map((function(e){return Number(e.humidity)})),o=[{x:n,y:l,name:"temperature",type:"scatter"}],u=[{x:n,y:c,name:"humidity",type:"scatter"}],i=Math.max.apply(Math,Object(m.a)(l)),d=Math.min.apply(Math,Object(m.a)(l)),p=Math.max.apply(Math,Object(m.a)(c)),s={autosize:!1,width:500,height:500,paper_bgcolor:"rgba(0,0,0,0)",plot_bgcolor:"rgba(0,0,0,0)",title:{text:"Temperatur [&deg;C]",font:{family:"Courier New, monospace",size:20,color:"#000"},xref:"paper",x:.05},yaxis:{range:[d-5,i+5]}},b={autosize:!1,width:500,height:500,paper_bgcolor:"rgba(0,0,0,0)",plot_bgcolor:"rgba(0,0,0,0)",title:{text:"Luftfuktighet [%]",font:{family:"Courier New, monospace",size:20,color:"#000"},xref:"paper",x:.05},yaxis:{range:[Math.min.apply(Math,Object(m.a)(c))-15,p+15]}},f={useresizehandler:!0};return r.a.createElement("div",{className:a},r.a.createElement(h.a,{data:o,layout:s,config:f}),r.a.createElement(h.a,{data:u,layout:b,config:f}))},s=function(e){var t=e.data,a=t.map((function(e){return Number(e.temperature)})),n=t.map((function(e){return Number(e.humidity)})),l=Math.max.apply(Math,Object(m.a)(a)),c=Math.min.apply(Math,Object(m.a)(a)),o=Math.max.apply(Math,Object(m.a)(n)),u=Math.min.apply(Math,Object(m.a)(n));return r.a.createElement("table",null,r.a.createElement("thead",null,r.a.createElement("tr",{className:"table_header"},r.a.createElement("th",{id:"borderboth"}," Storhet [enhet] "),r.a.createElement("th",{id:"borderboth"}," Min "),r.a.createElement("th",{id:"borderbottom"}," Max "))),r.a.createElement("tbody",null,r.a.createElement("tr",null,r.a.createElement("td",{id:"borderboth"}," Temperatur [\xb0C] "),r.a.createElement("td",{id:"borderboth"},"  ",c,"          "),r.a.createElement("td",{id:"borderbottom"},"  ",l,"                           ")),r.a.createElement("tr",null,r.a.createElement("td",{id:"borderright"}," Luftfuktighet [%]   "),r.a.createElement("td",{id:"borderright"}," ",u,"           "),r.a.createElement("td",null,"  ",o,"                             "))))},b=(a(30),a(31),a(32),a(33),a(34),a(35),a(17)),f=a.n(b),E=function(){return f.a.get("/api/data").then((function(e){return e.data}))},g=function(){var e=Object(n.useState)([]),t=Object(o.a)(e,2),a=t[0],l=t[1],c=Object(n.useState)([]),m=Object(o.a)(c,2),d=m[0],h=m[1];Object(n.useEffect)((function(){E().then((function(e){l(e),h(e)}))}),[]);var b=function(e){var t=48*-e;h(a.slice(t))};return r.a.createElement("div",{className:"wrapper"},r.a.createElement(u,null),r.a.createElement("h1",null,"V\xe4xthuset"),r.a.createElement("h3",null,"Measurements for 2020 started on 2020-03-29"),r.a.createElement("h2",null,"Temperatur och luftfuktighet"),r.a.createElement("div",{className:"plotbuttons"},r.a.createElement("button",{onClick:function(){return b(1)}},"1 dygn"),r.a.createElement("button",{onClick:function(){return b(2)}}," 2 dygn"),r.a.createElement("button",{onClick:function(){return b(7)}},"7 dygn"),r.a.createElement("button",{onClick:function(){return b(30)}},"30 dygn")),r.a.createElement(p,{data:d,className:"plots"}),r.a.createElement("h2",null,"Extremv\xe4rden senaste 7 dagar"),r.a.createElement(s,{data:a}),r.a.createElement(i,null))};c.a.render(r.a.createElement(g,null),document.getElementById("root"))}},[[18,1,2]]]);
//# sourceMappingURL=main.7bf7643e.chunk.js.map