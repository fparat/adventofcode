fn closing_of(c: char) -> char {
    match c {
        '(' => ')',
        '[' => ']',
        '{' => '}',
        '<' => '>',
        _ => unreachable!(),
    }
}

fn cost(c: char) -> i32 {
    match c {
        ')' => 3,
        ']' => 57,
        '}' => 1197,
        '>' => 25137,
        _ => unreachable!(),
    }
}

fn is_opening(c: char) -> bool {
    matches!(c, '(' | '[' | '{' | '<')
}

fn read_next(s: &mut impl Iterator<Item = char>, opening: char) -> i32 {
    loop {
        let next = s.next();
        match next {
            Some(c) if is_opening(c) => match read_next(s, c) {
                0 => continue,
                score => return score,
            },
            Some(c) if c == closing_of(opening) => return 0,
            Some(c) => return cost(c),
            None => break,
        }
    }
    0
}

fn part1(input: &str) {
    let score = input
        .lines()
        .map(|line| {
            let mut s = line.chars();
            let first = s.next().unwrap();
            read_next(&mut s, first)
        })
        .sum::<i32>();

    println!("Part 1: {}", score);
}

fn main() {
    let filename = std::env::args()
        .nth(1)
        .unwrap_or_else(|| "input".to_string());
    let input = std::fs::read_to_string(&filename).unwrap();

    part1(&input);
}
