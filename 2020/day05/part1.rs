fn select_high(range: (u32, u32)) -> (u32, u32) {
    let half = (range.1 - range.0 + 1) / 2;
    (range.0 + half, range.1)
}

fn select_low(range: (u32, u32)) -> (u32, u32) {
    let half = (range.1 - range.0 + 1) / 2;
    (range.0, range.1 - half)
}

fn to_coordinates(line: &str) -> (u32, u32) {
    let mut row = (0, 127);
    let mut col = (0, 7);

    for letter in line.chars() {
        match letter {
            'F' => row = select_low(row),
            'B' => row = select_high(row),
            'L' => col = select_low(col),
            'R' => col = select_high(col),
            _ => unreachable!(),
        }
    }

    assert_eq!(row.0, row.1);
    assert_eq!(col.0, col.1);

    (row.0, col.0)
}

fn to_id(coord: (u32, u32)) -> u32 {
    coord.0 * 8 + coord.1
}

fn line_id(line: &str) -> u32 {
    to_id(to_coordinates(line))
}

fn main() {
    let input = std::fs::read_to_string("input").unwrap();
    let max_id = input.lines().into_iter().map(line_id).max().unwrap();

    println!("Part 1: {}", max_id);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        assert_eq!(to_coordinates("BFFFBBFRRR"), (70, 7));
        assert_eq!(to_id((70, 7)), 567);
        assert_eq!(line_id("BFFFBBFRRR"), 567);

        assert_eq!(to_coordinates("FFFBBBFRRR"), (14, 7));
        assert_eq!(to_id((14, 7)), 119);
        assert_eq!(line_id("FFFBBBFRRR"), 119);

        assert_eq!(to_coordinates("BBFFBBFRLL"), (102, 4));
        assert_eq!(to_id((102, 4)), 820);
        assert_eq!(line_id("BBFFBBFRLL"), 820);
    }
}
