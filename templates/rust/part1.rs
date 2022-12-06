fn main() {
    let part1 = std::fs::read_to_string("input")
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
