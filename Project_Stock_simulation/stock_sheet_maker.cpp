#include <iostream>
#include <fstream>
#include <vector>
#include <string>
using namespace std;

struct Stock {
    int stock_id;
    string symbol;
    double market_price;
    double avg_buy;
    double avg_sell;
};

int main() {
    vector<Stock> stocks = {
        {101, "AAPL", 150.25, 149.80, 151.00},
        {102, "GOOG", 2800.50, 2795.00, 2810.00},
        {103, "TSLA", 720.00, 715.00, 725.00}
    };

    ofstream outFile("stock_sheet.csv");
    if (!outFile) {
        cerr << "Error opening file!" << endl;
        return 1;
    }

    // Header
    outFile << "stock_id,symbol,market_price,avg_buy,avg_sell\n";

    // Data
    for (const auto& stock : stocks) {
        outFile << stock.stock_id << "," << stock.symbol << ","
                << stock.market_price << "," << stock.avg_buy << ","
                << stock.avg_sell << "\n";
    }

    outFile.close();
    cout << "Stock sheet written successfully." << endl;
    return 0;
}
