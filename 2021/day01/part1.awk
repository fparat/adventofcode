BEGIN { p=999999; n=0 }
      { if ($1 > p) n += 1; }
      { p = $1 }
END   { print n }
