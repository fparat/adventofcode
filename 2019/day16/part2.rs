use std::env;
use std::fs;

const USAGE: &str = "./part1 INPUT";

fn main() {
    let path = env::args().nth(1).expect(USAGE);
    let input = fs::read_to_string(path)
        .expect("Unable to read file")
        .trim()
        .to_string();

    println!("Part2: {}", phase2(&input));
}

fn phase2(input: &str) -> String {
    let input_big = input.repeat(10000);
    let offset = input
        .chars()
        .take(7)
        .collect::<String>()
        .parse::<usize>()
        .unwrap();

    // The trick is that the pattern acts as a big "digit mask" in the second
    // half the vector: the pattern of factors looks like 0-0-...-0-1-1-...-1.
    // So if the offset points to this second half we can just sum the digits
    // starting from the position index.

    assert!(
        offset > input_big.len() / 2,
        "the following algorithm only works if the offset point to the 2nd \
         half of the vector"
    );

    let mut data = split_digits(&input_big[offset..]);
    for _ in 0..100 {
        let mut s: i32 = data.iter().sum();
        let mut new_data = Vec::new();
        for idx in 0..data.len() {
            let d = s % 10;
            new_data.push(d);
            s -= data[idx];
        }
        data = new_data;
    }

    data.truncate(8);
    join_digits(&data)
}

fn split_digits(i: &str) -> Vec<i32> {
    i.chars().map(|c| c.to_digit(10).unwrap() as i32).collect()
}

fn join_digits(digits: &[i32]) -> String {
    digits
        .iter()
        .copied()
        .map(|d| std::char::from_digit(d as u32, 10).unwrap())
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_phase2() {
        assert_eq!(phase2("03036732577212944063491565474664"), "84462026");
        assert_eq!(phase2("02935109699940807407585447034323"), "78725270");
        assert_eq!(phase2("03081770884921959731165446850517"), "53553731");
    }
}
