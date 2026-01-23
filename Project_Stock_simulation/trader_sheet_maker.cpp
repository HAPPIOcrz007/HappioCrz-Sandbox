#include <iostream>
#include <fstream>
#include <vector>
#include <string>
using namespace std;

struct Trader {
    int trader_id;
    double cash;
    vector<int> holdings; // stock1, stock2, stock3...stockN
};

int main() {
    int numStocks = 3; // Example: stock1, stock2, stock3
    vector<Trader> traders = {
        {1, 100000, {50, 20, 0}},
        {2, 50000, {0, 10, 5}}
    };

    ofstream outFile("trader_sheet.csv");
    if (!outFile) {
        cerr << "Error opening file!" << endl;
        return 1;
    }

    // Header
    outFile << "trader_id";
    for (int i = 1; i <= numStocks; i++) {
        outFile << ",stock" << i;
    }
    outFile << ",CASH\n";

    // Data
    for (const auto& trader : traders) {
        outFile << trader.trader_id;
        for (int holding : trader.holdings) {
            outFile << "," << holding;
        }
        outFile << "," << trader.cash << "\n";
    }

    outFile.close();
    cout << "Trader sheet written successfully." << endl;
    return 0;
}
