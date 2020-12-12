
const NORTH: (i32, i32) = (0, 1);
const SOUTH: (i32, i32) = (0, -1);
const WEST: (i32, i32) = (-1, 0);
const EAST: (i32, i32) = (1, 0);

#[derive(Debug)]
struct Ship {
    pub direction: (i32, i32),
    pub position: (i32, i32),
}

impl Ship {
    fn new() -> Self {
        Ship {
            direction: EAST,
            position: (0, 0),
        }
    }

    fn move_dir(&mut self, direction: (i32, i32), value: i32) {
        self.position = (self.position.0 + (direction.0 * value), self.position.1 + (direction.1 * value));
    }

    fn move_forward(&mut self, value: i32) {
        self.move_dir(self.direction, value);
    }

    fn turn_left(&mut self, value: i32) {
        let steps = (value / 90) % 4;
        for _ in 0..steps {
            self.direction = match self.direction {
                NORTH => WEST,
                WEST => SOUTH,
                SOUTH => EAST,
                EAST => NORTH,
                _ => panic!("unexpected direction {:?}", self.direction),
            }
        }
    }

    fn turn_right(&mut self, value: i32) {
        let steps = (value / 90) % 4;
        for _ in 0..steps {
            self.direction = match self.direction {
                NORTH => EAST,
                EAST => SOUTH,
                SOUTH => WEST,
                WEST => NORTH,
                _ => panic!("unexpected direction {:?}", self.direction),
            }
        }
    }

    fn run(&mut self, instruction: &str) {
        let op = instruction.chars().next().unwrap();
        let value = str::parse::<i32>(&instruction[1..]).unwrap();
        match op {
            'N' => self.move_dir(NORTH, value),
            'S' => self.move_dir(SOUTH, value),
            'E' => self.move_dir(EAST, value),
            'W' => self.move_dir(WEST, value),
            'L' => self.turn_left(value),
            'R' => self.turn_right(value),
            'F' => self.move_forward(value),
            _ => panic!("unexpected op {:?}", op),
        }
    }

    fn manhattan_distance(&self) -> i32 {
        self.position.0.abs() + self.position.1.abs()
    }
}

fn main() {
    let input = std::fs::read_to_string("input").unwrap();

    let mut ship = Ship::new();
    for line in input.lines() {
        ship.run(line);
    }

    println!("Part 1: {}", ship.manhattan_distance());

}


#[cfg(test)]
mod tests {
    use core::panic;

    use super::*;

    #[test]
    fn test_example() {
        let mut ship = Ship::new();
        let sample = "F10
N3
F7
R90
F11";
        for line in sample.lines() {
            ship.run(line)
        }

        println!("ship {:?}", &ship);

        assert_eq!(ship.manhattan_distance(), 25);
    }
}
