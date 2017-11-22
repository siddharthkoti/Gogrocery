var Suggest=function(){  //ctor
			temp=this;		//'this' refers to obj hence temp refers to obj
			this.timer=null;
			this.search=null;
			this.container=null;//global
			this.to=null;
			this.getCity=function(id){
				
				if(this.timer){
				
					clearTimeout(this.timer);
				}
				

				this.timer=setTimeout(this.sendTerm,1000,id);    //setTimeout() belongs to window object so this in sendterm refers to window object , hence use temp in sendTerm

			}

			this.global_product_details = [];
			this.sendTerm=function(id){
				
				temp.search=document.getElementById(id);
				temp.container=document.getElementById("contai" + id);
				temp.container.innerHTML="";
				console.log(temp.search.value);
				//temp.container.style.display="block";
				//console.log(this); //o/p in console:window
				//console.log(temp);
				url = "/get_list_of_products?occurrence="+ temp.search.value;
				//Empty?
				if(temp.search.value==""){
					console.log("No term...Empty term")
				
				}
				
				else{
					//Cache?
					console.log(localStorage.getItem("http://127.0.0.1:5000"+url));
					if(localStorage.getItem("http://127.0.0.1:5000"+url)){
					



						products = JSON.parse(localStorage.getItem("http://127.0.0.1:5000"+url));
						
						keys = Object.keys(products);
						// var products = [];

						// for(var i =0 ; i < r.length;i++){

						// 	products[i] = r[i][0];
						// }	
						

						console.log("fetching from cache");
						temp.populateCities(keys);
					}

					else{
						//Send
						console.log("NOT FOUND IN CACHE");						
						temp.xhr=new XMLHttpRequest();
						//url="http://localhost/ajax/day11/getCities_php.php?term=" + temp.search.value;
						temp.xhr.onreadystatechange=temp.fetchCities;
						temp.xhr.open("GET",url,true);
						temp.xhr.send();
					}
				}
			
			}
			
			this.fetchCities=function(){
				//this is temp.xhr

				if(this.readyState==4 && this.status==200){
					//var resp =JSON.parse(this.responseText);
					products = JSON.parse(this.responseText);
					keys = Object.keys(products);	
					console.log(products);
					// var cities = [];

					// for(var i =0 ; i < resp.length;i++){

					// 	cities[i] = resp[i][0];
					// }

					if(keys.length==0){
						temp.container.className="hidden";
						temp.container.style.overflowY="hidden";
						
					}
					else{
						temp.container.className="contai"; 
						localStorage.setItem(this.responseURL,this.responseText);
						console.log(this.responseURL);
						temp.populateCities(keys);
					}	
				}
				
			}
			
			this.populateCities=function(r){
				temp.container.style.overflowY="auto";
				temp.container.className="contai";
				
				for(var i=0; i<r.length; i++){
					d=document.createElement("div");
					d.className = "disp";
					
					d.innerHTML = r[i];
					d.onclick = this.setCity;

					d.onmouseover = this.highlightCity;
					d.onmouseout = this.undoHighlight;
					temp.container.appendChild(d);
				}
			}
			
			this.setCity=function(e){
				//console.log(e.target);
				//temp.to.className="show";
				// temp.to.style.zIndex=1;
				temp.search.value=e.target.innerHTML;
				console.log(temp.search.id.substring(7));

				var sgst = (products[e.target.innerHTML][2]) /2;
				cgst = sgst;
				$('#cost' + temp.search.id.substring(7)).val(products[e.target.innerHTML][1])
				$('#sgst' + temp.search.id.substring(7)).val(sgst)
				$('#cgst' + temp.search.id.substring(7)).val(cgst)


				//temp.container.style.overflowY="hidden";

				temp.container.innerHTML="";
				temp.container.className="hidden";
				//temp.container.style.display="none";

				
			}
			this.highlightCity=function(e){
				//console.log(e.target);
				e.target.style.backgroundColor="#BBBBBB";
				//temp.container.style.display="none";
				
			}
			this.undoHighlight=function(e){
				//console.log(e.target);
				e.target.style.backgroundColor="#F0E8E8";
				//temp.container.style.display="none";
				
			}
			
			
		}
				
obj=new Suggest();  //create object obj