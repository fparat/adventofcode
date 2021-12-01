BEGIN { p=999999; n=0 }
      { s[NR-1] += $1; s[NR-2] += $1; s[NR-3] += $1; }
END   {
      for(i=0; i<NR-2; i++) {
            if ( s[i] > p ) {
                  n += 1;
            }
            p = s[i];
      }
      print n;
}
