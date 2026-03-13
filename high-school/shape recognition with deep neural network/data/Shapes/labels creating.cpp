#include<fstream>
#include<iostream>
#include<string>
using namespace std;

int main(){
    string names[3] = {"heart", "circle", "triangle"};
    ofstream labels("labels_train.csv", ios::out | ios::trunc);
    if(labels.is_open()){
        for(int i = 0; i < 3; i ++){
            for (int j = 0; j < 400; j ++){
                labels << names[i] << j << ".jpg, " << i << "\n";
            }
        }
        cout << "succeeded" << endl;
    }
    else{
        cout << "file opening failed" << endl;
    }
}
