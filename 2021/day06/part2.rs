use std::collections::HashMap;

fn fish_run(input: &str, days: i64) -> i64 {
    let mut fishes = HashMap::new();

    input
        .trim()
        .split(',')
        .map(|s| s.parse::<i64>().unwrap())
        .for_each(|n| *fishes.entry(n).or_insert(0i64) += 1);

    for _ in 1..=days {
        let mut next_fishes = HashMap::new();
        for (&timer, &count) in fishes.iter() {
            if timer == 0 {
                *next_fishes.entry(6).or_insert(0) += count;
                *next_fishes.entry(8).or_insert(0) += count;
            } else {
                *next_fishes.entry(timer - 1).or_insert(0) += count;
            }
        }
        fishes = next_fishes;
    }

    let num_fishes = fishes.into_values().sum();

    num_fishes
}

fn part1(input: &str) {
    let num_fishes = fish_run(input, 80);
    println!("Part 1: {}", num_fishes);
}

fn part2(input: &str) {
    let num_fishes = fish_run(input, 256);
    println!("Part 2: {}", num_fishes);
}

fn main() {
    let filename = std::env::args()
        .nth(1)
        .unwrap_or_else(|| "input".to_string());
    let input = std::fs::read_to_string(&filename).unwrap();

    part1(&input);
    part2(&input);
}
