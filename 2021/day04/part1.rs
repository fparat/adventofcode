use std::str::FromStr;

#[derive(Debug)]
struct Board {
    lines: Vec<Vec<i32>>,
    marked: Vec<(i32, i32)>, // Vec<(row, col)>
}

impl Board {
    fn new(lines: Vec<Vec<i32>>) -> Board {
        let marked = Vec::new();
        Board { lines, marked }
    }

    fn size(&self) -> (i32, i32) {
        (self.lines.len() as i32, self.lines[0].len() as i32)
    }

    fn draw(&mut self, number: i32) -> bool {
        let mut win = false;
        for (row, line) in self.lines.iter().enumerate() {
            for (col, value) in line.iter().copied().enumerate() {
                if value == number {
                    self.marked.push((row as i32, col as i32));
                    win = self.is_win();
                }
            }
        }
        win
    }

    fn is_win(&self) -> bool {
        let (rows, cols) = self.size();

        for row in 0..rows {
            if self.marked.iter().copied().filter(|m| m.0 == row).count() as i32 >= rows {
                return true;
            }
        }

        for col in 0..cols {
            if self.marked.iter().copied().filter(|m| m.1 == col).count() as i32 >= cols {
                return true;
            }
        }

        false
    }

    fn score(&self, n: i32) -> i32 {
        let sum = self
            .lines
            .iter()
            .enumerate()
            .map(|(row, line)| {
                line.iter()
                    .copied()
                    .enumerate()
                    .filter_map(|(col, value)| {
                        if !self.marked.contains(&(row as i32, col as i32)) {
                            Some(value)
                        } else {
                            None
                        }
                    })
                    .sum::<i32>()
            })
            .sum::<i32>();

        sum * n
    }
}

#[derive(Debug)]
struct Bingo {
    drawn: Vec<i32>,
    boards: Vec<Board>,
}

impl FromStr for Bingo {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut lines = s.lines();
        let drawn = lines
            .next()
            .unwrap()
            .split(',')
            .map(|n| n.parse::<i32>().unwrap())
            .collect();

        assert!(lines.next().unwrap().is_empty());

        let mut boards = Vec::new();
        let mut board = Vec::new();

        for line in lines {
            if line.is_empty() {
                boards.push(Board::new(board));
                board = Vec::new();
            } else {
                let row = line
                    .split_whitespace()
                    .map(|n| n.parse::<i32>().unwrap())
                    .collect();
                board.push(row);
            }
        }
        if !board.is_empty() {
            boards.push(Board::new(board));
        }

        let game = Bingo { drawn, boards };

        Ok(game)
    }
}

impl Bingo {
    fn part1(&mut self) -> i32 {
        for n in self.drawn.iter().copied() {
            for board in self.boards.iter_mut() {
                if board.draw(n) {
                    return board.score(n);
                }
            }
        }
        unreachable!()
    }
}

fn part1(input: &str) {
    let mut bingo = Bingo::from_str(input).unwrap();
    let result = bingo.part1();
    println!("Part1: {}", result);
}

fn main() {
    let filename = std::env::args()
        .nth(1)
        .unwrap_or_else(|| "input".to_string());
    let input = std::fs::read_to_string(&filename).unwrap();

    part1(&input);
}
