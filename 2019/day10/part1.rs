use std::cmp::Ordering;
use std::env;
use std::fs;

const USAGE: &str = "./part1 INPUT";

fn main() {
    let path = env::args().nth(1).expect(USAGE);
    let data = fs::read_to_string(path)
        .expect("Unable to read file")
        .trim()
        .to_string();

    // Parse the asteroid positions
    let positions = data
        .lines()
        .enumerate()
        .flat_map(|(x, line)| {
            line.chars()
                .enumerate()
                .filter_map(move |(y, pos)| match pos {
                    '#' => Some((x as i32, y as i32)),
                    '.' => None,
                    _ => panic!("Unexpected character {:?}", pos),
                })
        })
        .collect::<Vec<_>>();

    let max_visible = positions
        .iter()
        .map(|pos| {
            // Calculate angles of all other positions
            let mut angles = positions
                .iter()
                .filter(|&p| p != pos)
                .map(|p| {
                    let dx = (p.0 - pos.0) as f64;
                    let dy = (p.1 - pos.1) as f64;
                    dy.atan2(dx)
                })
                .collect::<Vec<_>>();

            // Count unique angles
            angles.sort_unstable_by(|a, b| a.partial_cmp(b).unwrap_or(Ordering::Equal));
            angles.dedup();
            angles.len()
        })
        .max()
        .expect("Best position not found");

    println!("Result: {}", max_visible);
}
