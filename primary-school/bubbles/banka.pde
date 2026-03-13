class banka {
  float x = random(0, width);
  float y = random(0, height);
  float r = 30;
  
  float kol1 = random(0, 255);
  float kol2 = random(0, 255);
  float kol3 = random(0, 255);
  
  float pr = 5;
  float zx = random(-pr, pr);
  float zy = random(-pr, pr);
  
  //float nzx = zx;
  //float nzy = zy;
  
  void sprawdz(int j){
    if(x - r > banki[j].x){
      if(y - r > banki[j].y){
        if(zx < 0) {
          if(zy < 0){
            //nzx = -zx;
            //nzy = -zy;
          }
          //else{
            
          //}
        }
      }
    }
  }
  
  void przemiesc(){
    //zx = nzx;
    //zy = nzy;
    if(x - r / 2 < 1){
      zx = -zx;
    }
    else if(x + r / 2 > width - 1){
      zx = -zx;
    }
    if(y - r / 2 < 1){
      zy = -zy;
    }
    else if(y + r / 2 > height - 1){
      zy = -zy;
    }
    x = x + zx;
    y = y + zy;
  }
  
  void rysuj(){
    stroke(kol1, kol2, kol3);
    fill(kol1, kol2, kol3, 100);
    ellipse(x, y, r, r);
  }
  
}
