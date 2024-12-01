{
    l[NR] = $1
    c[$2] += 1
}

END {
    for (i = 1 ; i <= length(l); i++) {
        sum += l[i] * c[l[i]]
    }
    print sum
}
