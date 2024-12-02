fn main() {
    let filename = std::env::args()
        .nth(1)
        .unwrap_or_else(|| "input".to_string());

    let part1 = std::fs::read_to_string(&filename)
        .unwrap()
        .lines()
        .count();

    println!("Part 1: {}", part1);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        assert!(false);
    }
}
