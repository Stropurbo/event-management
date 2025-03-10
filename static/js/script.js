document.addEventListener("DOMContentLoaded", function() {
    const catdropdown = document.getElementById("categoryDropdown");
    const catlist = document.getElementById("categoryList");
    const selectItem = document.querySelector(".selected");

    catdropdown.addEventListener("click", function(){
        catlist.classList.toggle('hidden')
    });

    document.querySelectorAll(".catItem").forEach(item => {
        item.addEventListener("click", function(){
            selectItem.textContent = this.textContent;
            catlist.classList.add('hidden')
        });
    });

    document.addEventListener("click", function(event){
        if(!catdropdown.contains(event.target)){
            catlist.classList.add('hidden')
        }
    })

});

document.getElementById("menu-toggle").addEventListener('click', function(){
    document.getElementById('menu').classList.toggle('hidden');
});
    


    
