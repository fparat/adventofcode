fn part1(input: &str) {
    let num_simples = input
        .lines()
        .map(|line| line.split_once('|').unwrap().1)
        .map(|line| line.split_whitespace())
        .flatten()
        .map(|w| w.trim())
        .filter(|w| !w.is_empty())
        .filter(|w| w.len() == 2 || w.len() == 3 || w.len() == 4 || w.len() == 7)
        .count();

    println!("Part 1: {}", num_simples);
}

fn main() {
    let filename = std::env::args()
        .nth(1)
        .unwrap_or_else(|| "input".to_string());
    let input = std::fs::read_to_string(&filename).unwrap();

    part1(&input);
}
