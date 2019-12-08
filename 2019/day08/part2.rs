use std::env;
use std::fmt;
use std::fs;
use std::ops::Deref;

const USAGE: &str = "part1 INPUT WIDTH HEIGHT";

const WIDTH: usize = 25;
const HEIGHT: usize = 6;

const BLACK: u8 = 0;
const WHITE: u8 = 1;
const TRANSPARENT: u8 = 2;

#[derive(Debug, Clone)]
struct Layer(Vec<u8>);

impl Layer {
    fn pixels(&self) -> &[u8] {
        &self.0
    }

    fn digit_num(&self, digit: u8) -> usize {
        self.pixels()
            .iter()
            .copied()
            .filter(|&p| p == digit)
            .count()
    }
}

impl Deref for Layer {
    type Target = Vec<u8>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

struct Image {
    width: usize,
    height: usize,
    layers: Vec<Layer>,
}

impl Image {
    fn from_str(data: &str, width: usize, height: usize) -> Result<Image, String> {
        let layers: Vec<Layer> = data
            .trim()
            .as_bytes()
            .chunks(width * height)
            .map(|chunk| {
                chunk
                    .iter()
                    .copied()
                    .map(|c| (c as char).to_digit(10).expect("Not a digit") as u8)
                    .collect()
            })
            .map(|v| Layer(v))
            .collect();

        Ok(Image {
            width,
            height,
            layers,
        })
    }

    fn size(&self) -> usize {
        self.width * self.height
    }

    fn layers(&self) -> &[Layer] {
        &self.layers
    }

    fn pixel(&self, layer: usize, row: usize, col: usize) -> Option<u8> {
        self.layers[layer].get(row * self.width + col).copied()
    }

    fn fewest_zeroes(&self) -> Option<&Layer> {
        self.layers().iter().min_by_key(|layer| layer.digit_num(0))
    }

    fn merge(&mut self) {
        if self.layers.len() <= 1 {
            return;
        }

        let mut merged = Vec::with_capacity(self.size());
        for p in 0..self.size() {
            let mut pixels = self
                .layers()
                .iter()
                .map(|l| l.pixels()[p])
                .skip_while(|&pix| pix == TRANSPARENT);
            merged.push(pixels.next().expect("No valid pixel"))
        }

        self.layers = vec![Layer(merged)];
    }
}

impl fmt::Debug for Image {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "Image(width={},height={},layers=[\n",
            self.width, self.height
        )?;
        for (l, _) in self.layers.iter().enumerate() {
            writeln!(f, "  L{}:", l + 1)?;
            for r in 0..self.height {
                write!(f, "    ")?;
                for c in 0..self.width {
                    write!(f, "{}", self.pixel(l, r, c).unwrap())?;
                }
                write!(f, "\n")?;
            }
        }
        write!(f, "])")?;
        Ok(())
    }
}

fn main() {
    let path = env::args().nth(1).expect(USAGE);
    let width = env::args()
        .nth(2)
        .and_then(|w| w.parse::<usize>().ok())
        .unwrap_or(WIDTH);
    let height = env::args()
        .nth(3)
        .and_then(|h| h.parse::<usize>().ok())
        .unwrap_or(HEIGHT);

    let data = fs::read_to_string(path)
        .expect("Unable to read file")
        .trim()
        .to_string();

    let mut img = Image::from_str(&data, width, height).expect("Cannot read image");
    img.merge();

    println!(
        "{}",
        format!("{:?}", img)
            .replace("1", " ")
            .replace("0", "\u{2588}")
    );
}
