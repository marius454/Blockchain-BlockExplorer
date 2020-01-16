let blocksDiv = document.createElement('div')
blocksDiv.setAttribute("class","blockList")
let blockList = document.createElement('ui')

for (i = 0; i < 5; i++){
	let entry = document.createElement('li')
	entry.innerHTML += "<a href=\"search.html\">" + String(i) + "</a>"
	blockList.appendChild(entry)
}
blocksDiv.appendChild(blockList)


console.log(blocksDiv)
document.body.appendChild(blocksDiv)
