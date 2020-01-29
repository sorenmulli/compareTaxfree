$(document).ready(function() {
	var counter = 0;
	$.ajax({
		url: "ComparedPrices.json",
		dataType: "json",
		success: function(data){
			$(data).each(function(index, items) {
				buildHeader( items['catagory'][0] );
				$(items['catagory'][1].items).each(function(indexx, item) {
					var itemString = "<tr>";
					console.log()
					itemString += buildName( item );
					itemString += buildBorderPrice( item );
					itemString += buildDanishPrice( item );
					itemString += buildCart( counter++ );
					itemString += "</tr>";
					$("#price_table").append(itemString);
				})
			});
		}
	});
});


function SearchTable(){
	var input, filter, table, tr, td, th, i, txtValue;
	input = document.getElementById("search_input");
	filter = input.value.toUpperCase().replace(" ", "");
	table = document.getElementById("price_table");
	tr = table.getElementsByTagName("tr");

	for(i = 0; i < tr.length; i++){
		td = tr[i].getElementsByTagName("td")[0];
		if(td) {
			txtValue = td.textContent || td.innerText;
			if(txtValue.toUpperCase().replace(" ", "").indexOf(filter) > -1){
				tr[i].style.display = "";
			} else {
				tr[i].style.display = "none";
			}
		}
	}
}

function CalculateTotal(){
	var counter = 0;
	var danPris = 0.0;
	var bordPris = 0.0;
	var numOfProds = 0;
	$(document).ready(function() {
		$.ajax({
			url: "ComparedPrices.json",
			dataType: "json",
			success: function(data){
				$(data).each(function(index, items) {
					$(items['catagory'][1].items).each(function(indexx, item){
						danPris += calcPrice(item.danishPrice, counter);
						bordPris += calcPrice(item.borderPrice, counter);
						numOfProds += parseInt(document.getElementById("item" + counter).value);
						//console.log(document.getElementById("item" + counter));
						counter++;
						//console.log(item.borderPrice)
					});
				});
				document.getElementById("danish_price").innerText = "Dansk Pris: " + danPris;
				document.getElementById("border_price").innerText = "Border Pris: " + bordPris;
			}
		});
	});
}

function findDist(){
	var postCode = document.getElementById("post_code").value;
	if(postCode.length != 4){
		document.getElementById("dist_info").innerText = "Ikke et dansk postnummer";
		return;
	}
	$.ajax({
		url: "distances.json",
		dataType: "json",
		success: function(data){
			$(data).each(function(index, postCodes){
				var obj = postCodes[postCode];
				if(typeof obj === 'undefined'){
					document.getElementById("dist_info").innerText = "Postnummeret blev ikke fundet";
					return;
				}
				$("#dist_table").append(updateDist(obj));
			})
		}
	});
}

function updateDist(obj){
	var name = ["gedser", "rodby", "fleggaard_east", "fleggaard_west"];
	var stringBuild = "";
	stringBuild += "<tr>";
	for(let i = 0; i < 4; i++){
		//console.log(obj['distance'][i]);
		stringBuild += "<td>"
		stringBuild += "Location: " + name[i];
		stringBuild += "\nDistance: " + obj['distance'][i];
		stringBuild += "</td>"

	}
	stringBuild += "</tr>";
	console.log(stringBuild);
	return stringBuild;

}

function seeLocalStorage(){
	console.log(localStorage.getItem("danPris"));
	console.log(localStorage.getItem("bordPris"));
}

function calcPrice(item, counter) {
	let price = parseInt(item);
	let num = parseInt(document.getElementById("item" + counter).value);
	if(isNaN(price)) return 0
	else return price*num;
}



function buildName( item ){
	return buildTD().replace("!", item.name);
}

function buildBorderPrice( item ){
	return buildTD().replace("!", item.borderPrice);
}

function buildDanishPrice( item ){
	return buildTD().replace("!", item.danishPrice);
}

function buildCart( indexx ){
	var buttonString = "";
	buttonString += buildPlusButt( indexx );
	buttonString += buildPriceField( indexx );
	buttonString += buildMinusButt( indexx );
	return buildTD().replace("!",buttonString);
}

function buildPlusButt(indexx){
	return "<button id = \"+" + indexx +"\" onclick = \"plusFunction(\'item"+indexx+"\')\"  >+</button>";
}

function buildPriceField(indexx){
	return "<input class = \"inputItem\" type = \"number\" id = \"item" + indexx + "\" value = \"0\">";
}

function buildMinusButt(indexx){
	return "<button id = \"-" + indexx + "\" onclick = \"minusFunction(\'item"+indexx+"\') \">-</button>";
}

function buildTD(){
	return "<td>!</td>";
}

function buildHeader(name){
	var header =
	"<th>"+
	name.id+
	"</th>"
	$("#price_table").append(header)
}

function plusFunction(inputId){
	document.getElementById(inputId).value++;
}

function minusFunction(inputId){
	document.getElementById(inputId).value--;
}
