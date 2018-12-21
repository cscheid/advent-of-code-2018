#include <iostream>
using namespace std;

int main(int argc, char **argv)
{
  size_t a = atoi(argv[0]), b, c, d, f;
  b = 0;

  int min_b = -1;
  do {
    c = b | 65536;
    b = 7902108;
    do {
      f = c & 255;
      b = b + f;
      b = b & 16777215;
      b = b * 65899;
      b = b & 16777215;
      if (256 > c)
        break;
      f = 0;
      do {
        d = f + 1;
        d = d * 256;
        if (d > c)
          break;
        f = f + 1;
      } while (1);
      c = f;
    } while (1);
    if (min_b == -1)
      min_b = b;
    if (b < min_b) {
      cout << "b: " << b << endl;
      min_b = b;
    }
      
    if (b == a) break;
  } while (1);
}
