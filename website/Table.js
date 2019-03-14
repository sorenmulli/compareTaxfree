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


$(document).ready(function() {
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
					itemString += buildCart( indexx );
					itemString += "</tr>";

					$("#price_table").append(itemString);
				})
			});
		}
	});
});

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
	return "<button id = \"+" + indexx + "\"> + </button>";
}

function buildPriceField(indexx){
	return "<input id = \"item" + indexx + "\" placeholder = \"currently empty\">";
}

function buildMinusButt(indexx){
	return "<button id = \"-" + indexx + "\" >	 - </button>";
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
