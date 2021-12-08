const ALL_CHARS: &str = "abcdefg";

fn part1(input: &str) {
    let num_simples = input
        .lines()
        .map(|line| line.split_once('|').unwrap().1)
        .map(|line| line.split_whitespace())
        .flatten()
        .map(|w| w.trim())
        .filter(|w| !w.is_empty())
        .filter(|w| w.len() == 2 || w.len() == 3 || w.len() == 4 || w.len() == 7)
        .count();

    println!("Part 1: {}", num_simples);
}

fn split_words(s: &str) -> Vec<&str> {
    s.split_whitespace().collect()
}

fn sort_chars(s: &str) -> String {
    let mut chars: Vec<_> = s.chars().collect();
    chars.sort_unstable();
    chars.iter().collect()
}

fn missing_chars(s: &str) -> impl Iterator<Item = char> + '_ {
    ALL_CHARS.chars().filter(|c| !s.contains(*c))
}

struct CodeMap {
    codes: [Option<String>; 10],
}

impl CodeMap {
    fn new() -> Self {
        CodeMap {
            codes: Default::default(),
        }
    }

    fn set(&mut self, digit: u8, code: &str) {
        self.codes[digit as usize] = Some(sort_chars(code));
    }

    fn get_digit(&self, code: &str) -> Option<u8> {
        let code = sort_chars(code);
        self.codes
            .iter()
            .enumerate()
            .find(|(_, n_code)| Some(code.as_str()) == n_code.as_deref())
            .map(|(n, _)| n as u8)
    }

    fn get_code(&self, digit: u8) -> Option<&str> {
        self.codes[digit as usize].as_deref()
    }

    fn code_is_two(&self, tested: &str, samples: &[&str]) -> bool {
        // len == 5 and bottom-right branch of 2 is present in all other digits
        tested.len() == 5
            && missing_chars(tested).any(|c| {
                samples
                    .iter()
                    .filter(|code| **code != tested)
                    .all(|code| code.contains(c))
            })
    }

    fn code_is_three(&self, tested: &str) -> bool {
        // len == 5 and all digits of (1) are present
        tested.len() == 5
            && self
                .get_code(1)
                .map(|one| one.chars().all(|c| tested.contains(c)))
                .unwrap_or(false)
    }

    fn code_is_five(&self, tested: &str) -> bool {
        // len == 5 and one of missing digit is missing in (6)
        tested.len() == 5
            && self
                .get_code(6)
                .map(|six| missing_chars(tested).any(|c| missing_chars(six).any(|c6| c6 == c)))
                .unwrap_or(false)
    }

    fn code_is_six(&self, tested: &str) -> bool {
        // len == 6 and the missing digit is present in (1)
        tested.len() == 6
            && self
                .get_code(1)
                .map(|one| missing_chars(tested).any(|c| one.contains(c)))
                .unwrap_or(false)
    }

    fn code_is_nine(&self, tested: &str) -> bool {
        // len == 6 and the missing digit is missing in (4)
        tested.len() == 6
            && self
                .get_code(4)
                .map(|four| missing_chars(tested).any(|c| missing_chars(four).any(|c4| c4 == c)))
                .unwrap_or(false)
    }

    fn code_is_zero(&self, tested: &str) -> bool {
        // len == 6 and the missing digit is present in (5)
        tested.len() == 6
            && self
                .get_code(5)
                .map(|five| missing_chars(tested).any(|c| five.contains(c)))
                .unwrap_or(false)
    }

    fn from_codes(codes: &[&str]) -> Self {
        let mut map = CodeMap::new();
        let mut remaining = codes.iter().map(|s| s.to_string()).collect::<Vec<_>>();

        while !remaining.is_empty() {
            let mut remaining2 = Vec::with_capacity(6);

            for code in remaining {
                if code.len() == 2 {
                    map.set(1, &code);
                } else if code.len() == 3 {
                    map.set(7, &code);
                } else if code.len() == 4 {
                    map.set(4, &code);
                } else if code.len() == 7 {
                    map.set(8, &code);
                } else if map.code_is_two(&code, codes) {
                    map.set(2, &code);
                } else if map.code_is_three(&code) {
                    map.set(3, &code);
                } else if map.code_is_five(&code) {
                    map.set(5, &code);
                } else if map.code_is_six(&code) {
                    map.set(6, &code);
                } else if map.code_is_nine(&code) {
                    map.set(9, &code);
                } else if map.code_is_zero(&code) {
                    map.set(0, &code);
                } else {
                    remaining2.push(code);
                }
            }
            remaining = remaining2;
        }

        map
    }
}

fn part2(input: &str) {
    let mut outputs = Vec::new();

    let samples: Vec<(Vec<&str>, Vec<&str>)> = input
        .lines()
        .map(|line| line.split_once('|').unwrap())
        .map(|(d, o)| (split_words(d), split_words(o)))
        .collect();

    for (digit_codes, digit_output) in samples {
        let map = CodeMap::from_codes(&digit_codes);
        let output = digit_output
            .iter()
            .map(|o| map.get_digit(o).unwrap())
            .rev()
            .enumerate()
            .map(|(i, d)| d as i32 * 10i32.pow(i as u32))
            .sum::<i32>();
        outputs.push(output)
    }

    let result = outputs.iter().sum::<i32>();

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
