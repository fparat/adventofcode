use std::str::FromStr;

#[derive(Debug, Clone, Copy)]
enum Fold {
    X(u16),
    Y(u16),
}

impl FromStr for Fold {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (direction, value_str) = s.split_once('=').unwrap();
        let value = value_str.parse().unwrap();
        let fold = match direction {
            d if d.ends_with('x') => Fold::X(value),
            d if d.ends_with('y') => Fold::Y(value),
            _ => panic!("invalid direction"),
        };
        Ok(fold)
    }
}

#[derive(Debug)]
struct Manual {
    /// (x, y)
    dots: Vec<(u16, u16)>,
    folds: Vec<Fold>,
}

impl Manual {
    fn print(&self) {
        let y_max = self.dots.iter().copied().map(|d| d.1).max().unwrap();
        let x_max = self.dots.iter().copied().map(|d| d.0).max().unwrap();

        println!();

        for y in 0..=y_max {
            for x in 0..=x_max {
                if self.dots.contains(&(x, y)) {
                    print!("#");
                } else {
                    print!(" ");
                }
            }
            println!();
        }
    }

    fn fold(&mut self) -> bool {
        match self.folds.pop() {
            None => return false,
            Some(Fold::X(v)) => {
                for (x, _) in self.dots.iter_mut() {
                    if *x > v {
                        *x -= 2 * (*x - v);
                    }
                }
            }
            Some(Fold::Y(v)) => {
                for (_, y) in self.dots.iter_mut() {
                    if *y > v {
                        *y -= 2 * (*y - v);
                    }
                }
            }
        }

        self.dots
            .sort_unstable_by_key(|(a, b)| (((*a) as u32) << 16) + (*b as u32));
        self.dots.dedup();

        true
    }
}

impl FromStr for Manual {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (dots_lines, folds_lines) = s.split_once("\n\n").unwrap();

        let dots = dots_lines
            .lines()
            .map(|line| {
                line.split_once(',')
                    .map(|(x, y)| (x.parse().unwrap(), y.parse().unwrap()))
                    .unwrap()
            })
            .collect::<Vec<_>>();

        let folds = folds_lines
            .lines()
            .map(|line| line.parse().unwrap())
            .rev()
            .collect::<Vec<_>>();

        let manual = Manual { dots, folds };
        Ok(manual)
    }
}

fn part1(input: &str) {
    let mut manual = input.parse::<Manual>().unwrap();
    //manual.print();
    manual.fold();
    //manual.print();
    let dots_num = manual.dots.len();
    println!("Part 1: {}", dots_num);
}

fn part2(input: &str) {
    let mut manual = input.parse::<Manual>().unwrap();

    while manual.fold() {}

    println!("Part 2:");
    manual.print();
}

fn main() {
    let filename = std::env::args()
        .nth(1)
        .unwrap_or_else(|| "input".to_string());
    let input = std::fs::read_to_string(&filename).unwrap();

    part1(&input);
    part2(&input);
}
