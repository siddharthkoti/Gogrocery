function fetch(){
		var formdata = { 'stock_gt' : $('input[name=stock_gt]').val(),
							'stock_lt' : $('input[name=stock_lt]').val(),
							'category' : $('input[name=category]').val()
		};
		$.ajax({
			url: '/all_products_filter',
			type: 'POST',
			data : $('form').serialize(),
			success: function(response){
				//console.log(response.list_of_data); //	IF using the jasonify
				console.log(response); //if using json.dumps({object})
				var obj = JSON.parse(response);
				console.log(obj);
				var s = "<tr><td>Item</td><td>Total Quantity Sold</td><td>price</td> <td>Total</td></tr>";
				for(var key in obj){
					s += "<tr><td>" + obj[key][0] + "</td><td>" + obj[key][1] +  "</td><td>" + obj[key][2]  + "</td><td>" + obj[key][3] +  "</td><td>" + obj[key][4]  + "</td><td>" + obj[key][5]+ "</td></tr>";
				}
				document.getElementById("into").innerHTML=s;
			},
			error: function(error){
				console.log(error);
			}
		});
	
}
