#include<iostream>
using namespace std;

int ruch(char pl[]){
    cout << "Podaj pole:";
    int pole;
    cin >> pole;
    if(pole > 0 && pole < 10 && pl[pole-1] == pole + 48)
        return pole;
    else if(pole < 1 || pole > 9){
        cout << "Podane pole nie istnieje." << endl;
        return ruch(pl);
    }
    else{
        cout << "To pole jest zajete." << endl;
        return ruch(pl);
    }
}

bool wygrana(char pl[], char zn, int gracz){
    if((pl[0] == zn & pl[1] == zn & pl[2] == zn) || (pl[3] == zn & pl[4] == zn & pl[5] == zn) ||
       (pl[6] == zn & pl[7] == zn & pl[8] == zn) || (pl[0] == zn & pl[3] == zn & pl[6] == zn) ||
       (pl[1] == zn & pl[4] == zn & pl[7] == zn) || (pl[2] == zn & pl[5] == zn & pl[8] == zn) ||
       (pl[0] == zn & pl[4] == zn & pl[8] == zn) || (pl[2] == zn & pl[4] == zn & pl[6] == zn)){
        for(int i = 0; i < 5; i++)
            cout << endl;
        cout << pl[0] << '|' << pl[1] << '|' << pl[2] << endl;
        cout << '-' << ' ' << '-' << ' ' << '-' << endl;
        cout << pl[3] << '|' << pl[4] << '|' << pl[5] << endl;
        cout << '-' << ' ' << '-' << ' ' << '-' << endl;
        cout << pl[6] << '|' << pl[7] << '|' << pl[8] << endl;
        cout << "Wygrywa Gracz " << gracz << "!" << endl;
        return 0;
       }
       return 1;
}

int main(){
    char pl[9];
    for(int i = 1; i < 10; i++)
        pl[i-1] = i + 48;
    bool gra = 1;
    int gracz = 1, pole;
    while(gra){
        cout << pl[0] << '|' << pl[1] << '|' << pl[2] << endl;
        cout << '-' << ' ' << '-' << ' ' << '-' << endl;
        cout << pl[3] << '|' << pl[4] << '|' << pl[5] << endl;
        cout << '-' << ' ' << '-' << ' ' << '-' << endl;
        cout << pl[6] << '|' << pl[7] << '|' << pl[8] << endl;
        cout << "Gracz " << gracz << endl;
        pole = ruch(pl);
        if(gracz == 1){
            pl[pole-1] = 'o';
            gra = wygrana(pl, 'o', gracz);
            gracz = 2;
        }
        else{
            pl[pole-1] = 'x';
            gra = wygrana(pl, 'x', gracz);
            gracz = 1;
        }
        for(int i = 0; i < 5; i++)
            cout << endl;
    }
}
