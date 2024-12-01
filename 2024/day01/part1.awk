{
    l[NR] = $1
    r[NR] = $2
}

END {
    n = asort(l)
    m = asort(r)
    if (n != m) { print "ERROR"; exit 1 }

    for (i = 1 ; i <= n; i++) {
        d = l[i] - r[i]
        sum += (d < 0 ? -d : d)
    }

    print sum
}
