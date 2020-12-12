
const NORTH: (i32, i32) = (0, 1);
const SOUTH: (i32, i32) = (0, -1);
const WEST: (i32, i32) = (-1, 0);
const EAST: (i32, i32) = (1, 0);

#[derive(Debug)]
struct ShipV1 {
    pub direction: (i32, i32),
    pub position: (i32, i32),
}

impl ShipV1 {
    fn new() -> Self {
        ShipV1 {
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

#[derive(Debug)]
struct ShipV2 {
    pub waypoint: (i32, i32),  // relative to ship
    pub position: (i32, i32),
}

impl ShipV2 {
    fn new() -> Self {
        Self {
            waypoint: (10, 1),
            position: (0, 0),
        }
    }

    fn move_dir(&mut self, direction: (i32, i32), value: i32) {
        self.waypoint = (self.waypoint.0 + (direction.0 * value), self.waypoint.1 + (direction.1 * value));
    }

    fn move_forward(&mut self, value: i32) {
        self.position = (self.position.0 + (self.waypoint.0 * value), self.position.1 + (self.waypoint.1 * value));
    }

    fn turn_left(&mut self, value: i32) {
        let steps = (value / 90) % 4;
        for _ in 0..steps {
            self.waypoint = (-self.waypoint.1, self.waypoint.0);
        }
    }

    fn turn_right(&mut self, value: i32) {
        let steps = (value / 90) % 4;
        for _ in 0..steps {
            self.waypoint = (self.waypoint.1, -self.waypoint.0);
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

    let mut ship = ShipV1::new();
    for line in input.lines() {
        ship.run(line);
    }

    println!("Part 1: {}", ship.manhattan_distance());

    let mut ship2 = ShipV2::new();
    for line in input.lines() {
        ship2.run(line);
    }

    println!("Part 2: {}", ship2.manhattan_distance());

}


#[cfg(test)]
mod tests {
    use core::panic;

    use super::*;

    #[test]
    fn test_example_1() {
        let mut ship = ShipV1::new();
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

    #[test]
    fn test_example_2() {
        let mut ship = ShipV2::new();
        let sample = "F10
N3
F7
R90
F11";
        for line in sample.lines() {
            ship.run(line);
            println!("{}: {:?}", line, &ship);
        }

        println!("ship {:?}", &ship);

        assert_eq!(ship.manhattan_distance(), 286);
    }

    #[test]
    fn test_turn_2() {
        let mut ship = ShipV2::new();
        ship.waypoint = (1, 2);
        println!("ship {:?}", &ship);

        ship.run("R90");
        println!("R90: {:?}", &ship);
        assert_eq!(ship.waypoint, (2, -1));
        ship.run("R90");
        println!("R90: {:?}", &ship);
        assert_eq!(ship.waypoint, (-1, -2));
        ship.run("R90");
        println!("R90: {:?}", &ship);
        assert_eq!(ship.waypoint, (-2, 1));
        ship.run("R90");
        println!("R90: {:?}", &ship);
        assert_eq!(ship.waypoint, (1, 2));

        ship.run("L90");
        println!("L90: {:?}", &ship);
        assert_eq!(ship.waypoint, (-2, 1));
        ship.run("L90");
        println!("L90: {:?}", &ship);
        assert_eq!(ship.waypoint, (-1, -2));
        ship.run("L90");
        println!("L90: {:?}", &ship);
        assert_eq!(ship.waypoint, (2, -1));
        ship.run("L90");
        println!("L90: {:?}", &ship);
        assert_eq!(ship.waypoint, (1, 2));
    }
}
