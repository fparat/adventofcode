fn main() {
    let filename = std::env::args()
        .nth(1)
        .unwrap_or_else(|| "input".to_string());

    let part1 = std::fs::read_to_string(&filename)
        .unwrap()
        .lines()
        .map(|line| {
            line.split_whitespace()
                .map(|level| level.parse().unwrap())
                .collect::<Vec<i32>>()
        })
        .map(|report| check_rule1(&report) && check_rule2(&report))
        .filter(|is_safe| *is_safe)
        .count();

    println!("Part 1: {}", part1);
}

fn check_rule1(report: &[i32]) -> bool {
    report
        .as_ref()
        .windows(2)
        .all(|pair| ((pair[1] - pair[0]) * (report[1] - report[0])) > 0)
}

fn check_rule2(report: &[i32]) -> bool {
    report
        .as_ref()
        .windows(2)
        .map(|pair| (pair[1] - pair[0]).abs())
        .all(|d| d >= 1 && d <= 3)
}
