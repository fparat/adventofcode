use std::collections::HashMap;

fn part1(input: &str) {
    let mut fishes = HashMap::new();

    input.trim().split(',').map(|s| s.parse::<i32>().unwrap())
        .for_each(|n| *fishes.entry(n).or_insert(0) += 1);

    dbg!(&fishes);

    const DAYS: i32 = 80;

    for day in 1..=DAYS {
        println!("-- day{}", day);
        let mut next_fishes = HashMap::new();
        for (&timer, &count) in fishes.iter() {
            if timer == 0 {
                *next_fishes.entry(6).or_insert(0) += count;
                *next_fishes.entry(8).or_insert(0) += count;
            } else {
                *next_fishes.entry(timer-1).or_insert(0) += count;
            }
        }
        fishes = next_fishes;

        dbg!(&fishes);
        let num_fishes : i32 = fishes.values().sum();
        println!("count: {}", num_fishes);
    }

    let num_fishes : i32 = fishes.into_values().sum();

    println!("Part 1: {}", num_fishes);
}

fn main() {
    let filename = std::env::args()
        .nth(1)
        .unwrap_or_else(|| "input".to_string());
    let input = std::fs::read_to_string(&filename).unwrap();

    part1(&input);
}
