int il = 10;
banka[] banki = new banka[il];

void setup(){
  size(800, 800);
  for(int i = 0; i < il; i++){
    banki[i] = new banka();
  }
}

void draw(){
  background(255);
  for(int i = 0; i < il; i++){
    //for(int j = 0; j < il; j++){
      //if(j != i){
      //banki[i].sprawdz(j);
     // }
  //}
    banki[i].przemiesc();
    banki[i].rysuj();
  }
}
