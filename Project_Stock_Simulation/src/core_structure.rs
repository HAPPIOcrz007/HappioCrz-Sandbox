// src/core_structure.rs
#![allow(dead_code)]

use std::mem;

/// 
/// [Command.txt] ⟶ [batch_order_generator] ⟶ [order_maker]
/// ↑   ────────────────────────────────────────────────────────↵
/// ↑   ↳⟶ [orders0<stock_id>.bin] or [orders1<stock_id>.bin]
/// ↑   ↳⟶ [matching_engine] ⟶ price_change
/// ↑                                       ↑
/// └──────── Human Readable ───────────────┘
/// 

/// 
/// [Command.txt] ⟹ we enter texted orders(human understandable format)
///  ⬨ format
///  {stock_id} {orders count} {gradient}
///  ⬨
///  {stock_id} --> to be moved
///  {orders count} --> sum of bids/asks total
///  {gradient} --> expected slove of price change +/- must be mentioned
/// 

/// 
/// [batch_order_generator] ⟹ based on the [Command.txt] makes orders
///                                  and passes to [order_maker]
/// 
/// [order_maker] ⟹ makes the orders to put into [orders0<stock_id>.bin]
///                          or [orders1<stock_id>.bin] based on order
/// 
/// [orders0<stock_id>.bin] ⟹ the Sell order book based on <stock_id>
/// [orders1<stock_id>.bin] ⟹ the Buy order book based on <stock_id>
/// 
/// [matching_engine] ⟹ does matchings and manages the orderbooks
///                              and send changes to <price_change>
/// 
/// price_change ⟹ the final output and feed of this whole system
/// 

#[repr(C, packed(1))]
#[derive(Debug, Clone, Copy)]
pub struct Order {
    pub price: u32,        // 4 bytes = 0 to 4 294 967 295 raw units ⟹ $ 42 . 9 M
    // accuracy is price / 1000
    // max price = 4 294 967 . 295
    pub volume: u32,       // 4 bytes = 0 to 4,294,967,295 raw units ⟹ 4 . 29 M units
    // accuracy is volume / 10 , 000
    // max price = 429 496 . 7295
    pub trader_id: u32,    // 4 bytes , max 4.29 B traders
    pub stock_id: u16,     // 2 bytes 65 . 5 k stocks
    pub flags: u8,
    // flags ⟹ 0 ⟹ SELL + GTC (default)
    // flags ⟹ 1 ⟹ BUY  + GTC (default)
    // flags ⟹ 2 ⟹ SELL + FOK
    // flags ⟹ 3 ⟹ BUY  + FOK
    // flags ⟹ 4 ⟹ SELL + IOC
    // flags ⟹ 5 ⟹ BUY  + IOC
    // flags ⟹ 6 ⟹ XXXXXXXXXX
    // flags ⟹ 7 ⟹ XXXXXXXXXX
    pub reserved: u8,      // to match 16 bytes, for future markings
    // total 16 bytes / order
}

impl Order {
    // --- --- --- --- --- --- --- --- --- ---
    // --- --- --- --- --- --- --- --- --- ---
    pub fn is_sell_gtc(&self) -> bool { self.flags == 0x00 }
    pub fn is_buy_gtc(&self) -> bool { self.flags == 0x01 }
    pub fn is_sell_fok(&self) -> bool { self.flags == 0x02 }
    pub fn is_buy_fok(&self) -> bool { self.flags == 0x03 }
    pub fn is_sell_ioc(&self) -> bool { self.flags == 0x04 }
    pub fn is_buy_ioc(&self) -> bool { self.flags == 0x05 }

    pub fn set_sell_gtc(&mut self) { self.flags = 0x00; }
    pub fn set_buy_gtc(&mut self) { self.flags = 0x01; }
    pub fn set_sell_fok(&mut self) { self.flags = 0x02; }
    pub fn set_buy_fok(&mut self) { self.flags = 0x03; }
    pub fn set_sell_ioc(&mut self) { self.flags = 0x04; }
    pub fn set_buy_ioc(&mut self) { self.flags = 0x05; }
    // --- --- --- --- --- --- --- --- --- ---
    // --- --- --- --- --- --- --- --- --- ---
    
    pub fn get_price(&self) -> f64 { self.price as f64 / 1000.0 }
    pub fn get_volume(&self) -> f64 { self.volume as f64 / 10000.0 }
    pub fn get_trader_id(&self) -> u32 { self.trader_id }
    pub fn get_stock_id(&self) -> u16 { self.stock_id }
    // --- --- --- --- --- --- --- --- --- ---
    // --- --- --- --- --- --- --- --- --- ---
    
    pub fn set_trader_id(&mut self, t: u32) {
        self.trader_id = t;
    }
    
    pub fn set_stock_id(&mut self, s: u16) {
        self.stock_id = s;
    }
}

#[repr(C)]
#[derive(Debug, Clone, Copy)]
pub struct BatchCommand {
    pub stock_id: u16,       // 2 bytes - max 65 535
    pub order_count: u16,    // 2 bytes - max 65 535
    pub gradient_x100: i16,  // 2 bytes - Gradient ×100 -327.68 to +327.67
    pub noise_x100: u16,     // 2 bytes - Noise factor ×100 (0 to 655.35)
    // Total: 2+2+2+2 = 8 bytes
}

impl BatchCommand {
    pub fn get_gradient(&self) -> f64 { self.gradient_x100 as f64 / 100.0 }
    
    pub fn set_gradient(&mut self, g: f64) {
        self.gradient_x100 = (g * 100.0) as i16;
    }
    
    pub fn get_noise(&self) -> f64 { self.noise_x100 as f64 / 100.0 }
    
    pub fn set_noise(&mut self, n: f64) {
        self.noise_x100 = (n * 100.0) as u16;
    }
}

#[repr(C, packed(1))]
#[derive(Debug, Clone, Copy)]
pub struct StockState {
    pub last_price: u32,   // 4
    pub last_volume: u32,  // 4
    pub bid_price: u32,    // 4
    pub ask_price: u32,    // 4
    pub bid_volume: u32,   // 4
    pub ask_volume: u32,   // 4
    pub day_high: u32,     // 4
    pub day_low: u32,      // 4
    // 32 bytes
}

#[repr(C, packed(1))]
#[derive(Debug, Clone, Copy)]
pub struct Match {
    pub buyer_ref: u64,  // 32b trader_id + 32b order_seq
    pub seller_ref: u64, // 32b trader_id + 32b order_seq
    // 16 bytes total
}

impl Match {
    // Getters
    pub fn buyer_id(&self) -> u32 { (self.buyer_ref >> 32) as u32 }
    pub fn buyer_seq(&self) -> u32 { (self.buyer_ref & 0xFFFFFFFF) as u32 }
    
    pub fn seller_id(&self) -> u32 { (self.seller_ref >> 32) as u32 }
    pub fn seller_seq(&self) -> u32 { (self.seller_ref & 0xFFFFFFFF) as u32 }
    
    // Setters
    pub fn set_buyer(&mut self, id: u32, seq: u32) {
        self.buyer_ref = ((id as u64) << 32) | (seq as u64);
    }
    
    pub fn set_seller(&mut self, id: u32, seq: u32) {
        self.seller_ref = ((id as u64) << 32) | (seq as u64);
    }
}

pub mod order_constants {
    // Fixed-point multipliers
    pub const PRICE_MULT: u32 = 100;
    pub const VOLUME_MULT: u32 = 1000;

    pub const COMMANDS_DIR: &str = "data_holders/commands/";
    pub const ORDERS_TEXT_DIR: &str = "data_holders/orders/text/";
    pub const ORDERS_BIN_DIR: &str = "data_holders/orders/bin/";
    pub const STATES_CURRENT_DIR: &str = "data_holders/states/currents/";
    pub const STATES_SNAPSHOT_DIR: &str = "data_holders/states/snapshots/";
    pub const MATCHING_DIR: &str = "data_holders/matching/";
    
    /// 
    /// flags ⟹ 0 ⟹ SELL + GTC (default)
    /// flags ⟹ 1 ⟹ BUY  + GTC (default)
    /// flags ⟹ 2 ⟹ SELL + FOK
    /// flags ⟹ 3 ⟹ BUY  + FOK
    /// flags ⟹ 4 ⟹ SELL + IOC
    /// flags ⟹ 5 ⟹ BUY  + IOC
    /// 
    pub const FLAG_SELLGTC: u8 = 0x00;
    pub const FLAG_BUYGTC: u8 = 0x01;
    pub const FLAG_SELLFOK: u8 = 0x02;
    pub const FLAG_BUYFOK: u8 = 0x03;
    pub const FLAG_SELLIOC: u8 = 0x04;
    pub const FLAG_BUYIOC: u8 = 0x05;
}

// Compile-time assertions
const _: [(); 16] = [(); mem::size_of::<Order>()];
const _: [(); 8] = [(); mem::size_of::<BatchCommand>()];
const _: [(); 32] = [(); mem::size_of::<StockState>()];
const _: [(); 16] = [(); mem::size_of::<Match>()];

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn assert_sizes() {
        assert_eq!(mem::size_of::<Order>(), 16);
        assert_eq!(mem::size_of::<BatchCommand>(), 8);
        assert_eq!(mem::size_of::<StockState>(), 32);
        assert_eq!(mem::size_of::<Match>(), 16);
    }

    #[test]
    fn assert_alignments() {
        assert_eq!(mem::align_of::<Order>(), 1);
        assert_eq!(mem::align_of::<StockState>(), 1);
        assert_eq!(mem::align_of::<Match>(), 1);
        assert!(mem::align_of::<BatchCommand>() <= 8);
    }
}