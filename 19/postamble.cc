
 done:
  e = e + 1; // this shouldn't be hard-coded
  if (e >= n_instructions) {
    cout << a << " "
         << b << " "
         << c << " "
         << d << " "
         << e << " " 
         << f << endl;
    exit(0);
  }
  if (b != prev_b) {
    prev_b = b;
    cout << "." << flush;
  }
  goto *instructions[e];
}
