const array = document.getElementsByTagName("editor_main")[0].getElementsByTagName("main_center")[0].getElementsByTagName("array")[0];

const wall = document.getElementsByTagName("editor_header")[0].getElementsByTagName("wall")[0]
const path = document.getElementsByTagName("editor_header")[0].getElementsByTagName("path")[0]

var selected_color = 1;

function select_wall(){
	selected_color = 1;
	wall.style.backgroundColor = "blue";
	path.style.backgroundColor = "white";
	wall.style.color = "white";
	path.style.color = "black";
}

function select_path(){
	selected_color = 0;
	path.style.backgroundColor = "blue";
	wall.style.backgroundColor = "white";
	path.style.color = "white";
	wall.style.color = "black";
}


var array_width = array.clientWidth;
var array_heigt = array.clientHeight;

var cols = 5;
var rows = 5;

function getPixelWidth(){
	var pixel_width
	
	if(array_width < array_heigt){
		pixel_width = array_width / rows;
	} else {
		if (cols <= rows){
			pixel_width = array_width / cols;			
		} else {
			pixel_width = array_heigt / rows;		
		}
	}	
	if (pixel_width < 10){
		pixel_width = 10;
	}	
	return pixel_width;
}

const col_field = document.getElementById('array_width');
const row_field = document.getElementById('array_height');


function renderArray() {
	array.innerHTML = ''
	cols = col_field.value
	rows = row_field.value
	for(let row = 0; row < rows; row++){
		let px = array.appendChild(document.createElement("row"));
		for(let col = 0; col < cols; col++){
			let py = px.appendChild(document.createElement("pixel"));	
			
			// Get & set pixel width
			var pixel_width = getPixelWidth();		
			
			py.style.width = pixel_width;
			py.style.height = pixel_width;
			
			if (row == 0 || row == rows - 1 || col == 0 || col == cols - 1){
				py.style.backgroundColor = "grey";
			} else if (row % 2 == 0 || col % 2 == 0){
				py.style.backgroundColor = "black";
			}
		}
		// Set height and width of row
		px.style.height = pixel_width;
		px.style.width = pixel_width * cols;
	}
}

renderArray()

col_field.addEventListener('blur', renderArray);
row_field.addEventListener('blur', renderArray);


wall.addEventListener('click', select_wall);
path.addEventListener('click', select_path);

var isClicked = false;

array.addEventListener('mousedown', function(e){
	isClicked = !isClicked;
});
array.addEventListener('mouseup', function(e){
	isClicked = !isClicked;
});


array.addEventListener('mouseover', function(e){
    var element = e.target;
	if (isClicked){
		if (element.tagName == 'PIXEL' && selected_color == 1){
			element.style.backgroundColor = "black";
		}
		else if (element.tagName == 'PIXEL' && selected_color == 0){		
			element.style.backgroundColor = "white";
		}
	}	
});

function getPixelIndex(pixel){
	parent_row = pixel.parentNode
	x = Array.prototype.indexOf.call(parent_row.children, pixel);
	y = Array.prototype.indexOf.call(parent_row.parentNode.children, parent_row);
	return [x, y]
}

array.addEventListener('click', function(e){
    var element = e.target;
	if (element.tagName == 'PIXEL'){
		pixelIndex = getPixelIndex(element)
		alert('x: ' + pixelIndex[0] + '\ny: ' + pixelIndex[1]);
	}
});