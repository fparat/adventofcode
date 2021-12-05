use std::cmp::{max, min};
use std::collections::HashMap;
use std::str::FromStr;

/// Ex. "12,23" -> (12, 23)
fn parse_coord(s: &str) -> (i32, i32) {
    s.split_once(',')
        .map(|(x, y)| (x.trim(), y.trim()))
        .map(|(x, y)| (x.parse::<i32>().unwrap(), y.parse::<i32>().unwrap()))
        .unwrap()
}

#[derive(Debug)]
struct Vent {
    start: (i32, i32),
    stop: (i32, i32),
}

impl Vent {
    fn is_horizontal(&self) -> bool {
        self.start.0 == self.stop.0
    }
    fn is_vertical(&self) -> bool {
        self.start.1 == self.stop.1
    }

    fn points(&self) -> Vec<(i32, i32)> {
        if self.is_horizontal() {
            let from = min(self.start.1, self.stop.1);
            let to = max(self.start.1, self.stop.1);
            (from..=to).map(|y| (self.start.0, y)).collect()
        } else if self.is_vertical() {
            let from = min(self.start.0, self.stop.0);
            let to = max(self.start.0, self.stop.0);
            (from..=to).map(|x| (x, self.start.1)).collect()
        } else {
            unreachable!()
        }
    }
}

impl FromStr for Vent {
    type Err = ();

    /// Ex. "12,23 -> 34,45" -> Ok(Vent { start: (12, 23), stop: (34, 45) })
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        s.split_once("->")
            .map(|(start, stop)| (parse_coord(start), parse_coord(stop)))
            .map(|(start, stop)| Vent { start, stop })
            .ok_or(())
    }
}

fn part1(input: &str) {
    let mut points = HashMap::new();

    input
        .lines()
        .map(|line| line.parse::<Vent>().unwrap())
        .filter(|vent| vent.is_horizontal() || vent.is_vertical())
        .map(|vent| vent.points())
        .flatten()
        .for_each(|point| *points.entry(point).or_insert(0) += 1);

    let num_overlapped = points.into_iter().filter(|&(_, n)| n >= 2).count();

    println!("Part1: {}", num_overlapped);
}

fn main() {
    let filename = std::env::args()
        .nth(1)
        .unwrap_or_else(|| "input".to_string());
    let input = std::fs::read_to_string(&filename).unwrap();

    part1(&input);
}
