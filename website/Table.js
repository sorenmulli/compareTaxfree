function SearchTable(){

	var input, filter, table, tr, td, i, txtValue;
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

function AddItem(id){
	var val = parseInt(document.getElementById(id).value);

	if(val < 1 || val == null){
		document.getElementById(id).value = 0;
	} else {
		document.getElementById(id).value = val + 1;
	}
}

function CalculateTotal(){
	var table = document.getElementById('price_table');
	var counter = 0
	var val;

	var danishTotal = 0;
	var borderTotal = 0;

	$.ajax({
		url: "ComparedPrices.json",
		dataType: "json",
		success: function(data){
			$(data).each(function(index, value) {
				$(value['catagory'][1].items).each(function(indexx, value) {
					val = document.getElementById(counter++);
					if(!isNaN(val) ) {
						danishTotal += parseInt(val) * value;


					}
				});
			});
		}
	});

	console.log(danishTotal)

}

//On load of website
$(document).ready(function() {
	$.ajax({
		url: "ComparedPrices.json",
		dataType: "json",
		success: function(data){
			$(data).each(function(index, items) {
				//value['catagory'][1]
				$(items['catagory'][1].items).each(function(indexx, value) {
					var item =
					"<tr><td>"
					+value.name
					+"</td><td>"
					+value.borderPrice
					+"</td><td>"
					+value.danishPrice
					+"</td><td>"
					+"<button type=\"button\" id = \"_"
					+ index
					+"\" onclick=\" AddItem("
					+ index
					+ ")\"> Plus </button>"
					+  "<input type=\"number\" id =\""
					+ index
					+"\" placeholder = \"0\">"
					+"<button type=\"button\" id = \"_"
					+ index
					+"\"> Minus </button>"
					+"<Button id = \"crt"
					+ index
					+ "\" > Add To Cart </Button>"
					+"</td></tr>"
					$("#price_table").append(item)
				});
			});

		}
	});
});
