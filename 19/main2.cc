#include <iostream>
using namespace std;

int main()
{
  size_t a=0, b=0, c=976, d=140, f=0;
  // size_t a=0, b=0, c=10551376, d=10550400, f=0;
  for (b=1; b<=c; ++b) {
    if (c % b == 0) {
      a += b;
      cout << a << " " << b << endl;
    }
  }
  cout << a << " "
       << b << " "
       << c << " "
       << d << " "
       << f << endl;
}

