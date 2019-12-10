use std::cmp::Ordering;
use std::env;
use std::f64::consts::{FRAC_PI_2, PI};
use std::fs;

const USAGE: &str = "./part1 INPUT";

type Position = (i32, i32);
type Angle = f64;

#[derive(Debug)]
struct Asteroid {
    position: Position,
    angle: Angle,
}

#[derive(Debug)]
struct Station {
    position: Position,
    asteroids: Vec<Asteroid>,
}

fn calculate_angle(origin: Position, other: Position) -> f64 {
    let dx = (other.0 - origin.0) as f64;
    let dy = (other.1 - origin.1) as f64;
    dy.atan2(dx)
}

fn calculate_distance(a: Position, b: Position) -> f64 {
    let dx = (b.0 - a.0) as f64;
    let dy = (b.1 - a.1) as f64;
    (dx.powi(2) + dy.powi(2)).sqrt()
}

fn main() {
    let path = env::args().nth(1).expect(USAGE);
    let data = fs::read_to_string(path)
        .expect("Unable to read file")
        .trim()
        .to_string();

    // Parse the asteroid positions
    let positions = data
        .lines()
        .enumerate()
        .flat_map(|(y, line)| {
            line.chars()
                .enumerate()
                .filter_map(move |(x, pos)| match pos {
                    '#' => Some((x as i32, y as i32)),
                    '.' => None,
                    _ => panic!("Unexpected character {:?}", pos),
                })
        })
        .collect::<Vec<_>>();

    // Construct the station at the best location
    let mut station = positions
        .iter()
        .map(|pos| Station {
            position: *pos,
            asteroids: positions
                .iter()
                .filter(|&p| p != pos)
                .map(|&p| Asteroid {
                    position: p,
                    angle: calculate_angle(*pos, p),
                })
                .collect(),
        })
        .max_by_key(|station| {
            let mut angles = station
                .asteroids
                .iter()
                .map(|asteroid| asteroid.angle)
                .collect::<Vec<_>>();
            // remove duplicates
            angles.sort_unstable_by(|a, b| a.partial_cmp(b).unwrap_or(Ordering::Equal));
            angles.dedup();
            angles.len()
        })
        .expect("Best position not found");

    // Position the laser up -> rotate all asteroid angles by pi/2
    for asteroid in station.asteroids.iter_mut() {
        asteroid.angle += FRAC_PI_2;

        // Clamp [0rad,2pi)
        while asteroid.angle < 0. {
            asteroid.angle += PI * 2.;
        }
        while asteroid.angle > 2. * PI {
            asteroid.angle -= PI * 2.;
        }
    }

    let station_position = station.position;

    // Sort targets by angle then distance
    station.asteroids.sort_by(|a, b| {
        a.angle
            .partial_cmp(&b.angle)
            .unwrap_or(Ordering::Equal)
            .then_with(|| {
                let ra = calculate_distance(station_position, a.position);
                let rb = calculate_distance(station_position, b.position);
                ra.partial_cmp(&rb).unwrap_or(Ordering::Equal)
            })
    });

    const DESTROYED: f64 = std::f64::INFINITY;
    let two_hundreds;
    let mut destroyed = 0;
    'search_n_destroy: loop {
        if station.asteroids.iter().all(|a| a.angle == DESTROYED) {
            panic!("Cannot reach 200 vaporizations");
        }
        let mut last = DESTROYED;
        for i in 0..station.asteroids.len() {
            if station.asteroids[i].angle != last {
                destroyed += 1;
                if destroyed == 200 {
                    two_hundreds = station.asteroids[i].position;
                    break 'search_n_destroy;
                }
                last = station.asteroids[i].angle;
                station.asteroids[i].angle = DESTROYED;
            }
        }
    }

    println!("Result: {}", two_hundreds.0 * 100 + two_hundreds.1);
}
