fn main() {
    let filename = std::env::args()
        .nth(1)
        .unwrap_or_else(|| "input".to_string());

    let input = std::fs::read_to_string(&filename).unwrap();

    let lines = input
        .lines()
        .map(|l| l.chars().collect::<Vec<_>>())
        .collect::<Vec<_>>(); // horizontal

    let peek = |y: isize, x: isize| -> Option<char> {
        if x < 0 || y < 0 {
            return None;
        }
        lines
            .get(y as usize)
            .and_then(|l| l.get(x as usize))
            .copied()
    };

    let grid_match = |y: isize, x: isize, dy: isize, dx: isize| -> bool {
        peek(y + (0 * dy), x + (0 * dx)) == Some('X')
            && peek(y + (1 * dy), x + (1 * dx)) == Some('M')
            && peek(y + (2 * dy), x + (2 * dx)) == Some('A')
            && peek(y + (3 * dy), x + (3 * dx)) == Some('S')
    };

    let mut part1 = 0;
    for (y, line) in lines.iter().enumerate() {
        for (x, _c) in line.iter().enumerate() {
            let xmatch = |dy, dx| grid_match(y as isize, x as isize, dx, dy);
            part1 += xmatch(-1, -1) as i32;
            part1 += xmatch(-1, 0) as i32;
            part1 += xmatch(-1, 1) as i32;
            part1 += xmatch(0, -1) as i32;
            part1 += xmatch(0, 1) as i32;
            part1 += xmatch(1, -1) as i32;
            part1 += xmatch(1, 0) as i32;
            part1 += xmatch(1, 1) as i32;
        }
    }

    println!("Part 1: {part1}");
}
