// Author: Berin
//
// This script must be executed from a web browser's console.

var total = 5;

function new_image() {
    var url = "https://thispersondoesnotexist.com/image";
    window.open(url,'_blank');
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function crawl_images() {
  var counter = 0;
  while (counter < total){
      counter++;
      console.log("Abrindo imagen " + counter + " de " + total);
      new_image();
      await sleep(3000);
  }

  console.log("Finalizado!")
}

crawl_images();
