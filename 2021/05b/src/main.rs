use std::cmp;
use std::collections::HashSet;
use std::io::{BufReader, BufRead};
use std::fs::File;

fn main() {
    let file = File::open("05.txt").unwrap();
    let mut grid_points = HashSet::new();
    let mut danger_points = HashSet::new();
    for input_line in BufReader::new(file).lines() {
        match input_line {
            Ok(input_line) => {
                let line = parse_line(&input_line).unwrap();
                for point in line.points() {
                    let key = (point.x, point.y);
                    if grid_points.contains(&key) {
                        danger_points.insert(key);
                    }
                    grid_points.insert(key);
                }
            }
            Err(_) => ()
        }
    }
    println!("{:?}", danger_points);
    println!("{}", danger_points.len());
}

#[derive(Debug, PartialEq)]
pub struct Point {
  pub x: u32,
  pub y: u32,
}

#[derive(Debug, PartialEq)]
pub struct Line {
  pub x1: u32,
  pub y1: u32,
  pub x2: u32,
  pub y2: u32,
}

trait Orientation {
    fn is_horizontal(&self) -> bool;
    fn is_vertical(&self) -> bool;
}

trait DiscreteLine {
    fn points(&self) -> Vec<Point>;
}

impl Orientation for Line {
    fn is_horizontal(&self) -> bool { self.y1 == self.y2 }
    fn is_vertical(&self) -> bool { self.x1 == self.x2 }
}

impl DiscreteLine for Line {
    fn points(&self) -> Vec<Point> {
        let xmin = cmp::min(self.x1, self.x2);
        let xmax = cmp::max(self.x1, self.x2);
        let mut xrange = xmin..=xmax;
        let invert_x = xmin == self.x2;

        let ymin = cmp::min(self.y1, self.y2);
        let ymax = cmp::max(self.y1, self.y2);
        let mut yrange = ymin..=ymax;
        let invert_y = ymin == self.y2;

        let mut points: Vec<Point> = Vec::new();
        let mut x: u32 = 0;
        let mut y: u32 = 0;
        loop {
            x = xrange.next().unwrap_or(x);
            let mut emit_x = x;
            if invert_x {
                emit_x = self.x1 + self.x2 - x; 
            }

            y = yrange.next().unwrap_or(y);
            let mut emit_y = y;
            if invert_y {
                emit_y = self.y1 + self.y2 - y; 
            }

            points.push(Point {x: emit_x, y: emit_y});
            if x == xmax && y == ymax {
                break
            }
        }
        points
    }
}

fn parse_point(input: &str) -> Result<Point, &str> {
  let mut components = input.splitn(2, ",");
  let x: u32 = components.next().unwrap().parse().unwrap();
  let y: u32 = components.next().unwrap().parse().unwrap();
  Ok(Point {x: x, y: y})
}

fn parse_line(input: &str) -> Result<Line, &str> {
  let mut components = input.splitn(2, " -> ");
  let origin = parse_point(components.next().unwrap()).unwrap();
  let destination = parse_point(components.next().unwrap()).unwrap();
  Ok(Line {x1: origin.x, y1: origin.y, x2: destination.x, y2: destination.y})
}

#[test]
fn test_parse_line() {
  assert_eq!(parse_line("6,4 -> 2,0"), Ok(Line {
    x1: 6,
    y1: 4,
    x2: 2,
    y2: 0,
  }));
}

#[test]
fn test_parse_point() {
  assert_eq!(parse_line("2,1 -> 2,1"), Ok(Line {
    x1: 2,
    y1: 1,
    x2: 2,
    y2: 1,
  }));
}

#[test]
fn test_line_to_points() {
  let line = Line {x1: 1, y1: 1, x2: 3, y2: 3};
  let expected = vec![
    Point {x: 1, y: 1},
    Point {x: 2, y: 2},
    Point {x: 3, y: 3},
  ];
  assert_eq!(line.points(), expected)
}

#[test]
fn test_line_to_points_opposite_diagonal() {
  let line = Line {x1: 3, y1: 1, x2: 1, y2: 3};
  let expected = vec![
    Point {x: 3, y: 1},
    Point {x: 2, y: 2},
    Point {x: 1, y: 3},
  ];
  assert_eq!(line.points(), expected)
}

#[test]
fn test_point_to_points() {
  let line = Line {x1: 2, y1: 1, x2: 2, y2: 1};
  let expected = vec![
    Point {x: 2, y: 1},
  ];
  assert_eq!(line.points(), expected)
}
