fn part1(input: &str) {
    let line_len = input.lines().next().unwrap().len();
    let mut v = vec![0; line_len];

    for line in input.lines() {
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
        .map(|n| if n > 0 { 1 } else { 0 })
        .enumerate()
        .map(|(i, d)| d * 2i32.pow(i as u32))
        .sum();

    let epsilon = ((1 << line_len) - 1) - gamma;

    println!("Part1: {} * {} = {}", gamma, epsilon, gamma * epsilon);
}

fn main() {
    let filename = std::env::args()
        .nth(1)
        .unwrap_or_else(|| "input".to_string());
    let input = std::fs::read_to_string(&filename).unwrap();

    part1(&input);
}
