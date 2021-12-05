use std::io::{BufReader, BufRead};
use std::fs::File;

fn main() {
    let mut pos = 0;
    let mut depth = 0;
    let file = File::open("02.txt").unwrap();
    for line in BufReader::new(file).lines() {
        let instruction = parse_instruction(&line.unwrap()).unwrap();
        pos += instruction.x;
        depth += instruction.y;
    }
    println!("{}", pos * depth);
}

#[derive(Debug, PartialEq)]
pub struct Instruction {
  pub x: i32,
  pub y: i32,
}

fn parse_instruction(input: &str) -> Result<Instruction, &str> {
  let mut components = input.splitn(2, " ");
  let instruction = components.next().unwrap();
  let magnitude: i32 = components.next().unwrap().parse().unwrap();
  match instruction {
    "forward" => Ok(Instruction {x: magnitude, y: 0}),
    "down" => Ok(Instruction {x: 0, y: magnitude}),
    "up" => Ok(Instruction {x: 0, y: 0 - magnitude}),
    _ => Err(input),
  }
}

#[test]
fn test_parse_instruction() {
  assert_eq!(parse_instruction("forward 15"), Ok(Instruction {
    x: 15,
    y: 0,
  }));
}
