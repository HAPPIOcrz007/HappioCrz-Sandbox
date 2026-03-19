// src/processers/batch_order_maker.rs
//! this code reads the file in COMMANDS_DIR and makes orders

// Add this line at the top to include the module
#[path = "../core_structure.rs"]
mod core_structure;

use std::env;
use std::fs::File;
use std::io::{self, BufRead, BufReader, Write};
use std::time::{SystemTime, UNIX_EPOCH};

use core_structure::BatchCommand;
use core_structure::order_constants::COMMANDS_DIR;

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 2 {
        eprintln!("Usage: {} <commands_file> [-o output_name]", args[0]);
        eprintln!("Example: {} commands1001", args[0]);
        eprintln!("         {} commands1001 -o 12345678", args[0]);
        std::process::exit(1);
    }
    
    // Check if commands.txt file is mentioned in terminal call
    let mut cmd_filename = args[1].clone();
    if !cmd_filename.ends_with(".txt") {
        cmd_filename.push_str(".txt");
    }
    
    let out_filename = if args.len() == 4 && args[2] == "-o" {
        format!("{}.bin", args[3])
    } else {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();
        
        // Simple timestamp format: seconds since epoch
        format!("orders_{}.bin", now)
    };
    
    println!("Output: {}", out_filename);
    
    let full_path = format!("{}{}", COMMANDS_DIR, cmd_filename);
    let cmd_file = match File::open(&full_path) {
        Ok(file) => file,
        Err(e) => {
            eprintln!("Failed to open {}: {}", full_path, e);
            std::process::exit(1);
        }
    };
    
    let reader = BufReader::new(cmd_file);
    let mut lines = reader.lines();
    
    // Read first line for stock_id
    let first_line = match lines.next() {
        Some(line) => line?,
        None => {
            eprintln!("Empty commands file");
            std::process::exit(1);
        }
    };
    
    let stock_id: u16 = match first_line.trim().parse() {
        Ok(id) => id,
        Err(_) => {
            eprintln!("Invalid stock_id format");
            std::process::exit(1);
        }
    };
    
    let out_file = match File::create(&out_filename) {
        Ok(file) => file,
        Err(e) => {
            eprintln!("Failed to create output file {}: {}", out_filename, e);
            std::process::exit(1);
        }
    };
    
    let mut writer = io::BufWriter::new(out_file);
    
    for line in lines {
        let line = line?;
        let parts: Vec<&str> = line.split_whitespace().collect();
        
        if parts.len() >= 3 {
            let gradient: f64 = match parts[0].parse() {
                Ok(g) => g,
                Err(_) => continue,
            };
            
            let order_count: i32 = match parts[1].parse() {
                Ok(count) => count,
                Err(_) => continue,
            };
            
            let noise: f64 = match parts[2].parse() {
                Ok(n) => n,
                Err(_) => continue,
            };
            
            let mut cmd = BatchCommand {
                stock_id,
                order_count: order_count as u16,
                gradient_x100: 0,
                noise_x100: 0,
            };
            
            cmd.set_gradient(gradient);
            cmd.set_noise(noise);
            
            println!("Generating {} orders with gradient {}, noise {}", 
                     order_count, gradient, noise);
            
            // Write the BatchCommand to binary file
            let cmd_bytes = unsafe {
                std::slice::from_raw_parts(
                    &cmd as *const BatchCommand as *const u8,
                    std::mem::size_of::<BatchCommand>()
                )
            };
            
            writer.write_all(cmd_bytes)?;
        }
    }
    
    writer.flush()?;
    println!("Done! Generated orders in {}", out_filename);
    
    Ok(())
}