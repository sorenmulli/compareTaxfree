



$(document).ready(function() {
	$.ajax({
		url: "ComparedPrices.json",
		dataType: "json",
		success: function(data){
			$(data).each(function(index, value) {
				//value['catagory'][1]
				$(value['catagory'][1].items).each(function(index, value) {
					var item = "<tr><td>"+value.name + "</td><td>" + value.borderPrice + "</td><td>" + value.danishPrice + "</td></tr>"
					$("#price_table").append(item)
				});
			});
		}
	});
});