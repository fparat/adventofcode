fn main() {
    let filename = std::env::args()
        .nth(1)
        .unwrap_or_else(|| "input".to_string());

    let reports = std::fs::read_to_string(&filename)
        .unwrap()
        .lines()
        .map(|line| {
            line.split_whitespace()
                .map(|level| level.parse().unwrap())
                .collect::<Vec<i32>>()
        })
        .collect::<Vec<_>>();

    let part1 = reports
        .iter()
        .map(|report| check_rule1(&report) && check_rule2(&report))
        .filter(|is_safe| *is_safe)
        .count();

    println!("Part 1: {}", part1);

    let part2 = reports
        .clone()
        .into_iter()
        .map(dampened)
        .map(|reports| {
            reports
                .into_iter()
                .any(|report| check_rule1(&report) && check_rule2(&report))
        })
        .filter(|is_safe| *is_safe)
        .count();

    println!("Part 2: {}", part2);
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

fn dampened(report: Vec<i32>) -> impl Iterator<Item = Vec<i32>> {
    std::iter::once(report.clone()).chain((0..report.len()).into_iter().map(move |index| {
        let mut new_report = report.clone();
        new_report.remove(index);
        new_report
    }))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_damperner() {
        assert_eq!(
            dampened(vec![1, 2, 3]).collect::<Vec<Vec<i32>>>(),
            vec![vec![1, 2, 3], vec![2, 3], vec![1, 3], vec![1, 2],]
        )
    }
}
