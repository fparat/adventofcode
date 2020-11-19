#![allow(dead_code, unused_variables)]

use std::env;
use std::fs;

const USAGE: &str = "./part1 INPUT";

const BASE_PATTERN: &[i32] = &[0, 1, 0, -1];

fn main() {
    let path = env::args().nth(1).expect(USAGE);
    let input = fs::read_to_string(path)
        .expect("Unable to read file")
        .trim()
        .to_string();

    let mut result = n_phases(&split_digits(&input), 100);
    result.truncate(8);
    println!("Part1: {}", join_digits(&result));
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

fn process_phase(input: &[i32]) -> Vec<i32> {
    input
        .iter()
        .copied()
        .enumerate()
        .map(|(idx, _)| {
            input
                .iter()
                .copied()
                .zip(get_pattern(idx, input.len()).into_iter())
                .map(|(digit, factor)| digit * factor)
                .sum::<i32>()
                .abs()
                % 10
        })
        .collect()
}

fn n_phases(input: &[i32], num: usize) -> Vec<i32> {
    let mut data = input.to_vec();
    for _ in 0..num {
        data = process_phase(&data);
    }
    data
}

fn get_pattern(index: usize, size: usize) -> Vec<i32> {
    BASE_PATTERN
        .iter()
        .copied()
        .flat_map(|x| std::iter::repeat(x).take(index + 1))
        .cycle()
        .skip(1)
        .take(size)
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_split_digits() {
        let digits = split_digits("12345678");
        let expected: Vec<i32> = vec![1, 2, 3, 4, 5, 6, 7, 8];
        assert_eq!(digits, expected);
    }

    #[test]
    fn test_get_pattern() {
        let pattern = get_pattern(1, 15);
        let expected = vec![0, 1, 1, 0, 0, -1, -1, 0, 0, 1, 1, 0, 0, -1, -1];
        assert_eq!(pattern, expected);

        let pattern = get_pattern(0, 6);
        let expected = vec![1, 0, -1, 0, 1, 0];
        assert_eq!(pattern, expected);
    }

    #[test]
    fn test_phase_1() {
        let input = vec![1, 2, 3, 4, 5, 6, 7, 8];

        let phase1 = process_phase(&input);
        let expected = vec![4, 8, 2, 2, 6, 1, 5, 8];
        assert_eq!(phase1, expected);

        let phase2 = process_phase(&phase1);
        let expected = vec![3, 4, 0, 4, 0, 4, 3, 8];
        assert_eq!(phase2, expected);

        let phase3 = process_phase(&phase2);
        let expected = vec![0, 3, 4, 1, 5, 5, 1, 8];
        assert_eq!(phase3, expected);

        let phase4 = process_phase(&phase3);
        let expected = vec![0, 1, 0, 2, 9, 4, 9, 8];
        assert_eq!(phase4, expected);
    }

    #[test]
    fn test_phase_2() {
        let input = "80871224585914546619083218645595";
        let expected = "24176176";
        let mut result = n_phases(&split_digits(input), 100);
        result.truncate(8);
        assert_eq!(result, split_digits(expected));

        let input = "19617804207202209144916044189917";
        let expected = "73745418";
        let mut result = n_phases(&split_digits(input), 100);
        result.truncate(8);
        assert_eq!(result, split_digits(expected));

        let input = "69317163492948606335995924319873";
        let expected = "52432133";
        let mut result = n_phases(&split_digits(input), 100);
        result.truncate(8);
        assert_eq!(result, split_digits(expected));
    }
}
