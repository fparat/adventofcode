fn marker_pos(buffer: &str) -> usize {
    buffer
        .as_bytes()
        .windows(4)
        .enumerate()
        .find(|(_, chars)| {
            chars[0] != chars[1]
                && chars[0] != chars[2]
                && chars[0] != chars[3]
                && chars[1] != chars[2]
                && chars[1] != chars[3]
                && chars[2] != chars[3]
        })
        .map(|(pos, _)| pos + 4)
        .expect("marker not found")
}

fn main() {
    let input = std::fs::read_to_string("input").unwrap();
    let pos = marker_pos(&input);
    println!("Part 1: {}", pos);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        assert_eq!(marker_pos("mjqjpqmgbljsphdztnvjfqwrcgsmlb"), 7);
        assert_eq!(marker_pos("bvwbjplbgvbhsrlpgdmjqwftvncz"), 5);
        assert_eq!(marker_pos("nppdvjthqldpwncqszvftbrmjlhg"), 6);
        assert_eq!(marker_pos("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"), 10);
        assert_eq!(marker_pos("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"), 11);
    }
}
