#include <iostream>
using namespace std;

int main() {
    int n;
    cout << "n ni kiriting: ";
    cin >> n;

    if (n > 0 && (n & (n - 1)) == 0) {
        cout << "ha" << endl;
    } else {
        cout << "yo'q" << endl;
    }

    return 0;
}
