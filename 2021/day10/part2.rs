fn closing_of(c: char) -> char {
    match c {
        '(' => ')',
        '[' => ']',
        '{' => '}',
        '<' => '>',
        _ => unreachable!(),
    }
}

fn score1(c: char) -> i64 {
    match c {
        ')' => 3,
        ']' => 57,
        '}' => 1197,
        '>' => 25137,
        _ => unreachable!(),
    }
}

fn score2(c: char) -> i64 {
    match c {
        ')' => 1,
        ']' => 2,
        '}' => 3,
        '>' => 4,
        _ => unreachable!(),
    }
}

fn is_opening(c: char) -> bool {
    matches!(c, '(' | '[' | '{' | '<')
}

fn read_next(s: &mut impl Iterator<Item = char>, opening: char) -> i64 {
    loop {
        let next = s.next();
        match next {
            Some(c) if is_opening(c) => match read_next(s, c) {
                0 => continue,
                score => return score,
            },
            Some(c) if c == closing_of(opening) => return 0,
            Some(c) => return score1(c),
            None => break,
        }
    }
    0
}

fn syntax_error_score(line: &str) -> i64 {
    let mut s = line.chars();
    let first = s.next().unwrap();
    read_next(&mut s, first)
}

fn part1(input: &str) {
    let score = input.lines().map(syntax_error_score).sum::<i64>();
    println!("Part 1: {}", score);
}

fn complete(s: &mut impl Iterator<Item = char>, opening: char) -> Option<i64> {
    loop {
        let next = s.next();
        match next {
            Some(c) if is_opening(c) => {
                let ret = complete(s, c);
                match ret {
                    None => continue,
                    Some(score) => {
                        return Some(score * 5 + score2(closing_of(opening)));
                    }
                }
            }
            Some(c) if c == closing_of(opening) => return None,
            Some(c) => panic!("syntax error {}", c),
            None => return Some(score2(closing_of(opening))),
        }
    }
}

fn part2(input: &str) {
    let mut scores = Vec::new();
    let incompletes = input.lines().filter(|l| syntax_error_score(l) == 0);

    for line in incompletes {
        let mut s = line.chars();
        let score = loop {
            let next = s.next().unwrap();
            if let Some(score) = complete(&mut s, next) {
                break score;
            }
        };
        scores.push(score);
    }

    scores.sort_unstable();
    let result = scores[(scores.len() - 1) / 2];
    println!("Part 2: {}", result);
}

fn main() {
    let filename = std::env::args()
        .nth(1)
        .unwrap_or_else(|| "input".to_string());
    let input = std::fs::read_to_string(&filename).unwrap();

    part1(&input);
    part2(&input);
}
