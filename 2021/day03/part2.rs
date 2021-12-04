fn get_gamma_epsilon(input: &[String]) -> (i32, i32) {
    let line_len = input.iter().next().unwrap().len();
    let mut v = vec![0; line_len];

    for line in input.iter() {
        for (i, c) in line.chars().enumerate() {
            match c {
                '0' => v[i] -= 1,
                '1' => v[i] += 1,
                _ => panic!("unexpected char {:?}", c),
            }
        }
    }

    let gamma: i32 = v
        .iter()
        .rev()
        .copied()
        .map(|n| if n >= 0 { 1 } else { 0 })
        .enumerate()
        .map(|(i, d)| d * 2i32.pow(i as u32))
        .sum();

    let epsilon = ((1 << line_len) - 1) - gamma;

    (gamma, epsilon)
}

fn part1(input: &str) {
    let (gamma, epsilon) = get_gamma_epsilon(&input.lines().map(String::from).collect::<Vec<String>>());
    println!("Part1: {} * {} = {}", gamma, epsilon, gamma * epsilon);
}

fn vec_drain_criteria<F: Fn(&str) -> bool>(v: &mut Vec<String>, predicate: F) {
    let mut i = 0;
    while i < v.len() {
        if v.len() == 1 {
            break;
        }
        if !predicate(&v[i]) {
            v.remove(i);
        } else {
            i += 1;
        }
    }
}

fn part2(input: &str) {
    let line_len = input.lines().next().unwrap().len();
    let mut oxygen = input.lines().map(String::from).collect::<Vec<_>>();
    let mut co2 = oxygen.clone();

    for i in 0..line_len {
        let (gamma, _) = get_gamma_epsilon(&oxygen);
        let (_, epsilon) = get_gamma_epsilon(&co2);
        let bit_idx = line_len - 1 - i;
        let bit_criteria_o2 = if ((gamma >> bit_idx) & 1) == 1 { '1' } else { '0' };
        let bit_criteria_co2 = if ((epsilon >> bit_idx) & 1) == 1 { '1' } else { '0' };

        vec_drain_criteria(&mut oxygen, |n| n.chars().nth(i).unwrap() == bit_criteria_o2);
        vec_drain_criteria(&mut co2, |n| n.chars().nth(i).unwrap() == bit_criteria_co2);
    }

    let oxygen_rating = i32::from_str_radix(&oxygen[0], 2).unwrap();
    let co2_rating = i32::from_str_radix(&co2[0], 2).unwrap();

    println!("Part2: {} * {} = {}", oxygen_rating, co2_rating, oxygen_rating * co2_rating);
}

fn main() {
    let filename = std::env::args()
        .nth(1)
        .unwrap_or_else(|| "input".to_string());
    let input = std::fs::read_to_string(&filename).unwrap();

    part1(&input);
    part2(&input);
}
