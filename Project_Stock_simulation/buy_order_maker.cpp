#include <iostream>
#include <fstream>
#include <vector>
using namespace std;

struct BuyOrder {
    double timestamp;
    int trader_id;
    int stock_id;
    double bid_price;
    int volume;
};

int main() {
    vector<BuyOrder> buyOrders = {
        {0.1, 1, 101, 150.25, 100},
        {0.2, 2, 102, 2800.50, 50},
        {0.3, 3, 103, 720.00, 20}
    };

    ofstream outFile("buy_sheet.bin", ios::binary);
    if (!outFile) {
        cerr << "Error opening file!" << endl;
        return 1;
    }

    for (const auto& order : buyOrders) {
        outFile.write(reinterpret_cast<const char*>(&order), sizeof(order));
    }

    outFile.close();
    cout << "Buy sheet written successfully." << endl;
    return 0;
}
