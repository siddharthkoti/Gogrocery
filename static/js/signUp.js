$(function(){
	$('button').click(function(){
		var user = $('#inputUsername').val();
		var pass = $('#inputPassword').val();
		$.ajax({
			url: '/signUpUser',
			data: $('form').seriali
			ze(),
			type: 'POST',
			success: function(response){
				//console.log(response.list_of_data); //	IF using the jasonify
				console.log(response); //if using json.dumps({object})
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});