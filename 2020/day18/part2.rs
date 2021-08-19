#[derive(Debug, Clone, Copy)]
enum Token {
    Value(i64),
    Add,
    Mul,
    ParStart,
    ParEnd,
}

impl Token {
    fn precedence(&self) -> Option<i32> {
        match self {
            Token::Add => Some(2),
            Token::Mul => Some(1),
            _ => None,
        }
    }
}

struct TokenStream {
    tokens: Vec<Token>,
    current: Option<Token>,
}

impl TokenStream {
    fn new(mut tokens: Vec<Token>) -> Self {
        tokens.reverse(); // revert for using pop() efficiently
        Self {
            tokens,
            current: None,
        }
    }

    fn current(&self) -> Option<Token> {
        self.current
    }

    fn next(&mut self) -> Option<Token> {
        let token = self.tokens.pop();
        self.current = token;
        self.current
    }
}

impl From<&str> for TokenStream {
    fn from(input: &str) -> Self {
        Self::new(tokenize(input))
    }
}

fn tokenize(input: &str) -> Vec<Token> {
    let mut s = input;
    let mut tokens = Vec::new();

    while let Some(c) = s.chars().next() {
        match c {
            c if c.is_digit(10) => {
                let span = s.chars().take_while(|x| x.is_digit(10)).count();
                let value = s[..span].parse::<i64>().unwrap();
                tokens.push(Token::Value(value));
                s = &s[span - 1..];
            }

            c if c.is_whitespace() => {}

            '+' => tokens.push(Token::Add),
            '*' => tokens.push(Token::Mul),
            '(' => tokens.push(Token::ParStart),
            ')' => tokens.push(Token::ParEnd),

            c => panic!("Unknown character {:?}", c),
        }

        s = &s[1..];
    }

    tokens
}

fn compute_atom(tokens: &mut TokenStream) -> i64 {
    let token = tokens.next();
    match token {
        Some(token) => match token {
            Token::Value(v) => v,
            Token::ParStart => {
                let res = compute_expr(tokens, 1);
                assert!(matches!(tokens.current(), Some(Token::ParEnd)));
                res
            }
            Token::ParEnd => todo!(),
            tok => panic!("unexpected operator {:?}", tok),
        },
        None => todo!(),
    }
}

fn compute_expr(tokens: &mut TokenStream, prec: i32) -> i64 {
    let mut res = compute_atom(tokens);

    tokens.next();

    while let Some(token) = tokens.current() {
        if matches!(token, Token::ParEnd) {
            break;
        }

        if token.precedence().expect("not an operator") < prec {
            break;
        }

        let rhs = compute_expr(tokens, prec + 1);

        match token {
            Token::Add => res += rhs,
            Token::Mul => res *= rhs,
            tok => panic!("{:?} is not an operator", &tok),
        }
    }

    res
}

fn calculate(input: &str) -> i64 {
    let mut tokens = TokenStream::from(input);
    compute_expr(&mut tokens, 1)
}

fn main() {
    let input_file = std::env::args()
        .nth(2)
        .unwrap_or_else(|| "input".to_string());

    let part2: i64 = std::fs::read_to_string(input_file)
        .unwrap()
        .lines()
        .map(calculate)
        .sum();

    println!("Part 2: {}", part2);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[rustfmt::skip]
    #[test]
    fn test_example() {
        assert_eq!(calculate("1 + 2 * 3 + 4 * 5 + 6"), 231);
        assert_eq!(calculate("1 + (2 * 3) + (4 * (5 + 6))"), 51);
        assert_eq!(calculate("2 * 3 + (4 * 5) "), 46);
        assert_eq!(calculate("5 + (8 * 3 + 9 + 3 * 4 * 3) "), 1445);
        assert_eq!(calculate("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) "), 669060);
        assert_eq!(calculate("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 "), 23340);
    }
}
