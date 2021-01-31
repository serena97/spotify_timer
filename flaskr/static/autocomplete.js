// heavily based from https://www.w3schools.com/howto/howto_js_autocomplete.asp
function autocomplete(inp) {
    var currentFocus;

    async function getPlaylists(val) {
        const res = await fetch(`http://localhost:5000/auth/search/${val}`, {
          method: 'get', 
          headers: { 'Content-Type': 'application/json' }, 
        })
        return res.json();
    }

    inp.addEventListener("input", async function(e) {
        var list, item, i, val = this.value;
        closeAllLists();
        if (!val) { return false;}
        currentFocus = -1;

        arr = await getPlaylists(val)

        list = document.createElement("DIV");
        list.setAttribute("id", this.id + "autocomplete-list");
        list.setAttribute("class", "autocomplete-items");

        this.parentNode.appendChild(list);
        for (i = 0; i < arr.length; i++) {
          if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
            item = document.createElement("DIV");
            item.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
            item.innerHTML += arr[i].substr(val.length);
            item.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
            item.addEventListener("click", function(e) {
                /*insert the value for the autocomplete text field:*/
                inp.value = this.getElementsByTagName("input")[0].value;
                /*close the list of autocompleted values,
                (or any other open lists of autocompleted values:*/
                closeAllLists();
            });
            list.appendChild(item);
          }
        }
    });
    inp.addEventListener("keydown", function(e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
          /*If the arrow DOWN key is pressed,
          increase the currentFocus variable:*/
          currentFocus++;
          /*and and make the current item more visible:*/
          addActive(x);
        } else if (e.keyCode == 38) { //up
          /*If the arrow UP key is pressed,
          decrease the currentFocus variable:*/
          currentFocus--;
          /*and and make the current item more visible:*/
          addActive(x);
        } else if (e.keyCode == 13) {
          /*If the ENTER key is pressed, prevent the form from being submitted,*/
          e.preventDefault();
          if (currentFocus > -1) {
            /*and simulate a click on the "active" item:*/
            if (x) x[currentFocus].click();
          }
        }
    });
    function addActive(x) {
      if (!x) return false;
      removeActive(x);
      if (currentFocus >= x.length) currentFocus = 0;
      if (currentFocus < 0) currentFocus = (x.length - 1);
      x[currentFocus].classList.add("autocomplete-active");
    }
    function removeActive(x) {
      for (var i = 0; i < x.length; i++) {
        x[i].classList.remove("autocomplete-active");
      }
    }
    function closeAllLists(elmnt) {
      /*close all autocomplete lists in the document,
      except the one passed as an argument:*/
      var x = document.getElementsByClassName("autocomplete-items");
      for (var i = 0; i < x.length; i++) {
        if (elmnt != x[i] && elmnt != inp) {
          x[i].parentNode.removeChild(x[i]);
        }
      }
    }
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}
  

autocomplete(document.getElementById("myInput"));