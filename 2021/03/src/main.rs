use std::io::{BufReader, BufRead};
use std::fs::File;

fn main() {
    let mut count: u32 = 0;
    let mut aggregates: Vec<u32> = vec![0; 12];

    let file = File::open("03.txt").unwrap();
    for line in BufReader::new(file).lines() {
        match line {
          Ok(line) => {
            for (index, character) in line.char_indices() {
              let bit: u32 = character.to_digit(2).unwrap();
              aggregates[index] += bit;
            }
            count += 1;
          },
          Err(_) => ()
        }
    }

    let gamma_bits: String = aggregates.iter().map(|sum| ((sum >= &(count / 2)) as u8).to_string()).collect::<Vec<String>>().join("");
    let gamma: u64 = u64::from_str_radix(&gamma_bits, 2).unwrap();

    let epsilon_bits: String = aggregates.iter().map(|sum| ((sum < &(count / 2)) as u8).to_string()).collect::<Vec<String>>().join("");
    let epsilon: u64 = u64::from_str_radix(&epsilon_bits, 2).unwrap();

    println!("{}", gamma * epsilon);
}
