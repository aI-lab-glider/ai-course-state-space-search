class Grid {
    constructor(width, height){
        this.width = width;
        this.height = height;
    }

    isBlank(){
        for (let r = 0; r < this.width; r++){
            for (let c = 0; c < this.height; c++){
                if (document.getElementById(r + "-" + c).className != 'unvisited'){
                    return false;
                }
            }
        }
        return true;
    }

    createBlank(){  
        let board = document.getElementById("board");
        for (let r = 0; r < this.width; r++){
            let row = document.createElement('tr');
            row.setAttribute("id", r);
            for (let c = 0; c < this.height; c++){
                let col = document.createElement('td');
                let id = r + "-" + c;
                col.setAttribute("id", id);
                col.setAttribute("class", "unvisited");
                row.appendChild(col);
            }
            board.appendChild(row);
        }
    }

    clearGrid(){
        document.getElementById('draw').setAttribute('class', 'nav-item nav-link');
        document.getElementById('clear').setAttribute('class', 'nav-item nav-link active');
        for (let r = 0; r < this.width; r++){
            for (let c = 0; c < this.height; c++){
                let id = r + "-" + c;
                document.getElementById(id).setAttribute("class", "unvisited");
            }
        }
    }

    drawGrid(walls, start, end) {
        document.getElementById('draw').setAttribute('class', 'nav-item nav-link active');
        document.getElementById('clear').setAttribute('class', 'nav-item nav-link');
        walls.forEach(wall => {
            document.getElementById(wall[0] + "-" + wall[1]).setAttribute('class', 'wall')
        });
        document.getElementById(start[0][0] + "-" + start[0][1]).setAttribute('class', 'start');
        document.getElementById(end[0][0] + "-" + end[0][1]).setAttribute('class', 'end');
    }

    drawPath(path){
        path.forEach(node =>{
            if (document.getElementById(node[0]+"-"+node[1]).getAttribute('class') == 'unvisited'){
                document.getElementById(node[0]+"-"+node[1]).setAttribute('class', 'visited');
            }
        });
    }
}

let grid = new Grid();

function drawBlank(){
    $.ajax({
        type: 'POST',
        url: 'search/draw',
        contentType: 'application/json',
        success: function(response){
            let board = document.getElementById("board");
            grid.width = response['size'][0][0];
            grid.height = response['size'][0][1];
            for (let r = 0; r < grid.width; r++){
                let row = document.createElement('tr');
                row.setAttribute("id", r);
                for (let c = 0; c < grid.height; c++){
                    let col = document.createElement('td');
                    let id = r + "-" + c;
                    col.setAttribute("id", id);
                    col.setAttribute("class", "unvisited");
                    row.appendChild(col);
                }
                board.appendChild(row);
            }
        },
        error: function(response){
            console.log(response);
        }
    });
}

function drawAll(){
    $.ajax({
        type: 'POST',
        url: 'search/draw',
        contentType: 'application/json',
        success: function(response){
            document.getElementById('info').innerHTML = "";
            grid.drawGrid(response['walls'], response['start'], response['finish']);
        },
        error: function(response){
            console.log(response);
        }
    });
};


function solution() {
    let algoUrl = "";
    let algo = document.getElementById('algorithm').value;
    // Switch statement is not working...
    if (algo == 1){
        algoUrl = "search/solvebfs";
    } else if (algo == 2){
        algoUrl = "search/solvedfs";
    } else if (algo == 3){
        algoUrl = "search/solvea";
    } else if (algo == 4){
        algoUrl = "search/solveida";
    }

    $.ajax({
        type: 'POST',
        url: algoUrl,
        contentType: 'application/json',
        success: function(response){
            if (!grid.isBlank()){
                document.getElementById('info').innerHTML = "";
                grid.drawPath(response['path']);
            } else {
                document.getElementById('info').innerHTML = "<h2>Draw walls first!</h2>";
            }
        },
        error: function(response){
            console.log(response);
        }
    });
};

function clearAll() {
    $.ajax({
        type: 'POST',
        url: 'search/clear',
        contentType: 'application/json',
        success: function(){
            grid.clearGrid();
        },
        error: function(response){
            console.log(response);
        }
    });
};
