// core_structure.h

/**
 * [Command.txt] ⟶ [batch_order_generator.cpp] ⟶ [order_maker.cpp]
 * ↑   ────────────────────────────────────────────────────────↵
 * ↑   ↳⟶ [orders0<stock_id>.bin] or [orders1<stock_id>.bin]
 * ↑   ↳⟶ [matchine_engine.cpp] ⟶ price_change
 * ↑                                       ↑
 * └──────── Human Readable ───────────────┘
*/

/**
 * [Command.txt] ⟹ we enter texted orders(human understandable format)
 *  ⬨ format
 *  {stock_id} {orders count} {gradient}
 *  ⬨
 *  {stock_id} --> to be moved
 *  {orders count} --> sum of bids/asks total
 *  {gradient} --> expected slove of price change +/- must be mentioned
*/

/**
 * [batch_order_generator.cpp] ⟹ based on the [Command.txt] makes orders
 *                                  and passes to [order_maker.cpp]
 * 
 * [order_maker.cpp] ⟹ makes the orders to put into [orders0<stock_id>.bin]
 *                          or [orders1<stock_id>.bin] based on order
 * 
 * [orders0<stock_id>.bin] ⟹ the Buy order book based on <stock_id>
 * [orders1<stock_id>.bin] ⟹ the Sell order book based on <stock_id>
 * 
 * [matchine_engine.cpp] ⟹ does matchings and manages the orderbooks
 *                              and send changes to <price_change>
 * 
 * price_change ⟹ the final output and feed of this whole system
 */

 