#[derive(Debug)]
enum Op {
    Add(Box<Node>, Box<Node>),
    Mul(Box<Node>, Box<Node>),
}

#[derive(Debug)]
enum Node {
    Value(i64),
    Op(Op),
}

#[derive(Debug)]
enum Token {
    Value(i64),
    Add,
    Mul,
    ParStart,
    ParEnd,
}

fn tokenize(input: &str) -> Vec<Token> {
    let mut s = input;
    let mut tokens = Vec::new();

    loop {
        match s.chars().next() {
            Some(c) => match c {
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
            },

            None => break,
        }

        s = &s[1..];
    }

    tokens
}

fn step_tree<'a>(
    nodes: Option<Box<Node>>,
    tokens: &mut impl Iterator<Item = &'a Token>,
) -> Option<Box<Node>> {
    let has_previous = nodes.is_some();

    let nodes = match tokens.next() {
        Some(token) => match token {
            Token::Value(v) => match nodes {
                Some(nodes) => panic!("unexpected nodes for value token: {:?}", nodes),
                None => Some(Box::new(Node::Value(*v))),
            },

            Token::Add => {
                let left = nodes.unwrap_or_else(|| step_tree(None, tokens).expect("no node"));
                let right = step_tree(None, tokens).expect("no node");
                Some(Box::new(Node::Op(Op::Add(left, right))))
            }

            Token::Mul => {
                let left = nodes.unwrap_or_else(|| step_tree(None, tokens).expect("no node"));
                let right = step_tree(None, tokens).expect("no node");
                Some(Box::new(Node::Op(Op::Mul(left, right))))
            }

            Token::ParStart => {
                let node = step_tree(None, tokens).expect("no node after (");
                step_tree(Some(node), tokens)
            }

            Token::ParEnd => return nodes,
        },
        None => return nodes,
    };

    if has_previous {
        step_tree(nodes, tokens)
    } else {
        nodes
    }
}

fn build_tree(tokens: &[Token]) -> Box<Node> {
    let mut token_it = tokens.iter();
    let node = step_tree(None, &mut token_it).expect("no first node");
    let nodes = step_tree(Some(node), &mut token_it).expect("no node");
    nodes
}

fn eval(tree: &Box<Node>) -> i64 {
    match &**tree {
        Node::Value(v) => *v,
        Node::Op(op) => match op {
            Op::Add(l, r) => eval(l) + eval(r),
            Op::Mul(l, r) => eval(l) * eval(r),
        },
    }
}

fn calculate(input: &str) -> i64 {
    let tokens = tokenize(input);
    let nodes = build_tree(&tokens);
    eval(&nodes)
}

fn main() {
    let part1: i64 = std::fs::read_to_string("input")
        .unwrap()
        .lines()
        .map(calculate)
        .sum();

    println!("Part 1: {}", part1);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[rustfmt::skip]
    #[test]
    fn test_example() {
        assert_eq!(calculate("1 + 2 * 3 + 4 * 5 + 6"), 71);
        assert_eq!(calculate("1 + (2 * 3) + (4 * (5 + 6))"), 51);
        assert_eq!(calculate("2 * 3 + (4 * 5) "), 26);
        assert_eq!(calculate("5 + (8 * 3 + 9 + 3 * 4 * 3) "), 437);
        assert_eq!(calculate("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) "), 12240);
        assert_eq!(calculate("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 "), 13632);
    }
}
