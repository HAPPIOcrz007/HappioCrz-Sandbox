#include <iostream>
#include <fstream>
#include <vector>
using namespace std;

struct SellOrder {
    double timestamp;
    int trader_id;
    int stock_id;
    double ask_price;
    int volume;
};

int main() {
    vector<SellOrder> sellOrders = {
        {0.1, 4, 101, 151.00, 80},
        {0.2, 5, 102, 2810.00, 40}
    };

    ofstream outFile("sell_sheet.bin", ios::binary);
    if (!outFile) {
        cerr << "Error opening file!" << endl;
        return 1;
    }

    for (const auto& order : sellOrders) {
        outFile.write(reinterpret_cast<const char*>(&order), sizeof(order));
    }

    outFile.close();
    cout << "Sell sheet written successfully." << endl;
    return 0;
}
