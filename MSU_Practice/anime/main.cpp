#include <stdio.h>
#include <iostream>
#include <fstream>
#include <cmath>
#include <string>
using namespace std;

int main()
{
    ofstream out;
    double x;


    out.open("C:\\Users\\Administrator.EliteBook-8760w\\Desktop\\Anime\\X.txt");

    if (out.is_open())
    {
        for(int i=0; i<300; i++)
        {
            x=i*0.1;
            out<<x<<" ";
        }
        out.close();
    }
    else
    {
        cout<<endl<<"Error opening file"<<endl;
    }


    for(int T=80; T<280; T++)
    {
        out.open("C:\\Users\\Administrator.EliteBook-8760w\\Desktop\\Anime\\Y"+to_string(T)+".txt");
        for(int i=0; i<300; i++)
        {
            x=i*0.1;
            out<<pow(-1,T)*sin(x*T/280)<<" ";
        }
        out.close();
    }


    cout<<"done";
    return 0;
}
