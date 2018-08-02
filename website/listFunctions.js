// Pseudo catagories until object is made in JSON-file
let catagories = ['beer', 'wine', 'spirits']

function makeDiv() {
  // Function to setup the divisions
  // Placing it in the division selection
  let output = '';
  let name;
  for (var i = 0; i < catagories.length; i++){
    // Naming each division as such: Catagory + 'List'
    name = catagories[i] + "list";
    output += "<ul class = 'product' id = '" + name + "'></ul>"
  };
  //Placing it in the <div id = "selection" innerHTML
  document.getElementById("selection").innerHTML = output;
};

function makeList (type, name) {
  listname = name + 'list';

  // Function to make list for each item in a list
  // Placing it in the respective id of the divisions
  var output = '';
  //Making a loop to run through every item.
  //Every item gets assigned to a <li></li>
  //The buttons will also be assigned here

  for (var i = 0; i < type.length; i++) {
    output +=
    // Title
    "<li>" + type[i].title + "<br>" +
    // Price
    type[i].price +
    "</li>" +
    //minusButton

    //input
    "<input type = 'text' id = '" + name + i +"'>"
    //plusButton

    ;

    //Making the title


  };
  document.getElementById(listname).innerHTML = output;
};

//plusButton
function plusButt() {

};

//minusButton
function minusButt() {

};
