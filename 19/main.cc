#include <iostream>
using namespace std;

int main()
{
  // int a=0, b=0, c=976, d=140, f=0;
  size_t a=0, b=0, c=10551376, d=10550400, f=0;
  do {
    f = 1;
    do {
      d = b * f;
      if (d == c) {
        a += b;
      }
      ++f;
    } while (f <= c);
    ++b;
  } while (b <= c);
  cout << a << " "
       << b << " "
       << c << " "
       << d << " "
       << f << endl;
}

