#include <stdio.h>
#include <iostream>
#include <fstream>
#include <cmath>
using namespace std;

int main()
{
    ofstream out;
    double x;
    double y;
    int i;
    int j;


    out.open("X.txt");
    if (out.is_open())
    {
        for(j=0; j<200; j++){
            for(i=0; i<200; i++)
            {
               x=-10+i*0.1;
               out<<x<<" ";
            }
            out<<endl;
        }
        out.close();
    }
    else
    {
        cout<<endl<<"Error opening file"<<endl;
    }

    out.open("Y.txt");
    if (out.is_open())
    {
        for(i=0; i<200; i++)
        {
              x=-10+i*0.1;
              for(j=0; j<200; j++)
              {
                out<<x<<" ";
              }
              out<<endl;
        }
        out.close();
    }
    else
    {
        cout<<endl<<"Error opening file"<<endl;
    }

    out.open("Z.txt");
    if (out.is_open())
    {
        for(i=0; i<200; i++)
        {
            y=-10+i*0.1;
            for(j=0; j<200; j++)
            {
              x=-10+j*0.1;
              out<<x*x-y*y<<" ";
            }
            out<<endl;
        }
        out.close();
    }
    else
    {
        cout<<endl<<"Error opening file"<<endl;
    }

    cout<<"done";
    return 0;
}
