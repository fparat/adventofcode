fn part1(input: &str) {
    let mut pos = (0, 0);
    input
        .lines()
        .map(|line| line.split_once(' ').unwrap())
        .for_each(|(op, val)| {
            let val = val.parse::<i32>().unwrap();
            match op {
                "forward" => pos.0 += val,
                "up" => pos.1 -= val,
                "down" => pos.1 += val,
                _ => panic!("unknown op {}", op),
            }
        });

    println!("Part1: {}", pos.0 * pos.1);
}

fn part2(input: &str) {
    let mut pos = (0, 0);
    let mut aim = 0;

    input
        .lines()
        .map(|line| line.split_once(' ').unwrap())
        .for_each(|(op, val)| {
            let val = val.parse::<i32>().unwrap();
            match op {
                "forward" => {
                    pos.0 += val;
                    pos.1 += aim * val;
                },
                "up" => aim -= val,
                "down" => aim += val,
                _ => panic!("unknown op {}", op),
            }
        });
    println!("Part2: {}", pos.0 * pos.1);
}

fn main() {
    let filename = std::env::args().nth(1).unwrap_or_else(|| "input".to_string());
    let input = std::fs::read_to_string(&filename).unwrap();

    part1(&input);
    part2(&input);
}
